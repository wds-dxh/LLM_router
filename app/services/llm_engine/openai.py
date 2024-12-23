import os
import json
from datetime import datetime
from typing import Dict, Any, AsyncGenerator, Optional, ClassVar, List, Tuple
from collections import deque  # 用于实现固定大小的历史记录
from openai import AsyncOpenAI
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from .base import BaseLLMEngine

class OpenAIEngine(BaseLLMEngine):
    """OpenAI引擎实现"""
    
    _client: ClassVar[AsyncOpenAI] = None
    _prompts: ClassVar[Dict[str, str]] = None
    MAX_HISTORY = 10  # 最大历史记录数
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._init_client()
        self._load_prompts()
        self._init_conversation_settings()

    def _init_conversation_settings(self):
        """初始化对话设置"""
        self.conversation_context = {}
        self.max_turns = self.config.get('conversation', {}).get('max_turns', 10)
        self.truncate_mode = self.config.get('conversation', {}).get('truncate_mode', 'sliding')
        # 从文件加载历史记录
        self._load_conversation_history()

    def _load_prompts(self) -> None:
        """加载提示词模板"""
        try:
            prompts_path = self.config['storage']['prompts_path']
            prompts_dir = os.path.dirname(prompts_path)

            # 确保目录存在
            if not os.path.exists(prompts_dir):
                os.makedirs(prompts_dir)

            # 默认提示词
            default_prompts = {
                "default": "You are a helpful assistant.",
                "professional": "You are a professional assistant with expertise in various fields.",
                "creative": "You are a creative assistant that helps with brainstorming.",
                "code": "You are a coding assistant that helps with programming.",
                "儿童心理专家": "你是一个儿童心理专家，擅长儿童心理健康和发展指导。",
                "知心大姐姐": "你是一个知心大姐姐，擅长心理疗愈和心理疏导。"
            }

            # 如果文件不存在或为空，创建新文件
            if not os.path.exists(prompts_path) or os.path.getsize(prompts_path) == 0:
                with open(prompts_path, 'w', encoding='utf-8') as f:
                    json.dump(default_prompts, f, indent=4, ensure_ascii=False)
                OpenAIEngine._prompts = default_prompts
                print(f"Created default prompts file at: {prompts_path}")
                return

            # 尝试加载现有文件
            try:
                with open(prompts_path, 'r', encoding='utf-8') as f:
                    loaded_prompts = json.load(f)
                    if not loaded_prompts:  # 如果加载的数据为空
                        raise ValueError("Empty prompts file")
                    # print(loaded_prompts) 调试用
                    OpenAIEngine._prompts = loaded_prompts
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error loading prompts file: {e}")
                print("Using default prompts instead.")
                # 备份损坏的文件（如果存在）
                if os.path.exists(prompts_path):
                    backup_path = f"{prompts_path}.backup"
                    os.rename(prompts_path, backup_path)
                # 创建新的默认文件
                with open(prompts_path, 'w', encoding='utf-8') as f:
                    json.dump(default_prompts, f, indent=4, ensure_ascii=False)
                OpenAIEngine._prompts = default_prompts

        except Exception as e:
            print(f"Unexpected error in _load_prompts: {e}")
            OpenAIEngine._prompts = {"default": "You are a helpful assistant."}

    def _validate_config(self) -> None:
        required_fields = ['api_key', 'base_url', 'model']
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"Missing required field: {field}")

    def _init_client(self) -> None:
        """初始化OpenAI客户端"""
        if OpenAIEngine._client is None:
            OpenAIEngine._client = AsyncOpenAI(
                api_key=self.config['api_key'],
                base_url=self.config.get('base_url', "https://api.chatanywhere.tech"),
                timeout=httpx.Timeout(self.config.get('timeout', 30.0))
            )

    def _truncate_context(self, context: List[Dict]) -> List[Dict]:
        """截断对话上下文"""
        if len(context) <= 1:  # 只有system消息
            return context
            
        turns = (len(context) - 1)   # 如果有多轮对话，每轮对话有两条消息
        if turns <= self.max_turns: # 对话轮数未超过最大值
            return context
            
        if self.truncate_mode == 'clear':
            return [context[0]]
        else:  # sliding mode
            preserved_messages_count = self.max_turns * 2
            return [context[0]] + context[-preserved_messages_count:]

    def _get_user_role_key(self, user_id: str) -> str:
        """生成用户角色的唯一键"""
        return f"{user_id}_{self.current_role}"

    def _load_conversation_history(self):
        """从文件加载最近的对话历史"""
        try:
            conversations_path = self.config['storage']['conversations_path']
            if os.path.exists(conversations_path):
                with open(conversations_path, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    for user_role_key, messages in history.items():
                        # 解析用户ID和角色
                        user_id, role = user_role_key.split('_', 1)
                        # 只保留最近的MAX_HISTORY条消息作为上下文
                        recent_messages = []
                        for conv in messages[-self.MAX_HISTORY:]:
                            recent_messages.extend(conv['messages'])
                        if recent_messages:
                            system_prompt = self._prompts.get(role, self._prompts["default"])
                            self.conversation_context[user_role_key] = [
                                {"role": "system", "content": system_prompt}
                            ] + recent_messages
        except Exception as e:
            print(f"Error loading conversation history: {e}")

    async def chat(self, user_id: str, message: str, context: Optional[list] = None) -> Dict[str, Any]:
        """执行对话"""
        user_role_key = self._get_user_role_key(user_id)
        
        # 初始化或更新用户上下文
        if user_role_key not in self.conversation_context:
            system_prompt = self._prompts.get(self.current_role, self._prompts["default"])
            self.conversation_context[user_role_key] = [
                {"role": "system", "content": system_prompt}
            ]

        # 添加用户消息
        self.conversation_context[user_role_key].append(
            {"role": "user", "content": message}
        )

        try:
            response = await self._make_request(self.conversation_context[user_role_key])
            if not response["success"]:
                raise RuntimeError(response["error"])

            result = {
                'text': response["data"].choices[0].message.content,
                'role': "assistant",
                'raw_response': response["data"].model_dump()
            }

            # 添加助手回复到上下文
            self.conversation_context[user_role_key].append(
                {"role": "assistant", "content": result['text']}
            )

            # 保持上下文在最大限制内
            if len(self.conversation_context[user_role_key]) > self.MAX_HISTORY + 1:  # +1 是因为system消息
                self.conversation_context[user_role_key] = [
                    self.conversation_context[user_role_key][0]  # 保留system消息
                ] + self.conversation_context[user_role_key][-(self.MAX_HISTORY):]  # 保留最近的消息

            # 保存最近的对话到文件
            await self.save_conversation(user_id, [
                {"role": "user", "content": message},
                {"role": "assistant", "content": result['text']}
            ])

            return result
        except Exception as e:
            raise RuntimeError(f"Chat failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def _make_request(self, messages: List[Dict]) -> Dict:
        """发送请求到OpenAI API，带有重试机制"""
        try:
            encoded_messages = [
                {
                    "role": msg["role"],
                    "content": msg["content"].encode('utf-8').decode('utf-8')
                }
                for msg in messages
            ]
            
            response = await self._client.chat.completions.create(
                model=self.config['model'],
                messages=encoded_messages,
                temperature=self.config.get('temperature', 0.7),
                max_tokens=self.config.get('max_tokens', 500),
                top_p=self.config.get('top_p', 1.0)
            )
            return {"success": True, "data": response}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def chat_stream(self, user_id: str, message: str, context: Optional[list] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """流式对话"""
        messages = self._prepare_messages(message, context)
        try:
            response = await self._client.chat.completions.create(
                model=self.config['model'],
                messages=messages,
                temperature=self.config.get('temperature', 0.7),
                max_tokens=self.config.get('max_tokens', 500),
                top_p=self.config.get('top_p', 1.0),
                stream=True
            )
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield {
                        'text': chunk.choices[0].delta.content,
                        'type': 'content'
                    }
        except Exception as e:
            yield {'error': str(e), 'type': 'error'}

    def set_role(self, role_type: str) -> bool:
        if role_type in self._prompts:
            self.current_role = role_type
            return True
        return False

    def get_current_role(self) -> str:
        return self.current_role

    def list_available_roles(self) -> List[str]:
        return list(self._prompts.keys())

    async def save_conversation(self, user_id: str, conversation: List[Dict]) -> None:
        """保存对话历史到JSON文件（只保存最近的对话）"""
        try:
            conversations_path = self.config['storage']['conversations_path']
            if not os.path.exists(os.path.dirname(conversations_path)):
                os.makedirs(os.path.dirname(conversations_path))

            user_role_key = self._get_user_role_key(user_id)
            data = {
                "timestamp": datetime.now().isoformat(),
                "role": self.current_role,
                "messages": conversation
            }

            try:
                history = {}
                if os.path.exists(conversations_path):
                    with open(conversations_path, 'r', encoding='utf-8') as f:
                        try:
                            history = json.load(f)
                        except json.JSONDecodeError:
                            history = {}

                # 使用user_role_key作为键
                if user_role_key not in history:
                    history[user_role_key] = []
                history[user_role_key].append(data)
                
                # 限制每个用户角色组合的历史记录数量
                if len(history[user_role_key]) > self.MAX_HISTORY:
                    history[user_role_key] = history[user_role_key][-self.MAX_HISTORY:]

                with open(conversations_path, 'w', encoding='utf-8') as f:
                    json.dump(history, f, indent=2, ensure_ascii=False)

            except Exception as e:
                print(f"Error saving conversation: {e}")

        except Exception as e:
            print(f"Error accessing conversation file: {e}")

    async def get_conversation_history(self, user_id: str) -> List[Dict]:
        """获取对话历史"""
        try:
            conversations_path = self.config['storage']['conversations_path']
            if not os.path.exists(conversations_path):
                return []
            
            user_role_key = self._get_user_role_key(user_id)
            with open(conversations_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
                return history.get(user_role_key, [])
        except Exception as e:
            print(f"Error loading conversation history: {e}")
            return []

    def _prepare_messages(self, message: str, context: Optional[list] = None) -> list:
        """准备消息列表"""
        messages = context or []
        messages.append({"role": "user", "content": message})
        return messages

    def clear_context(self, user_id: str) -> None:
        """清除用户上下文"""
        user_role_key = self._get_user_role_key(user_id)
        if user_role_key in self.conversation_context:
            del self.conversation_context[user_role_key]

    def get_context_summary(self, user_id: str) -> Dict[str, Any]:
        """获取上下文摘要"""
        user_role_key = self._get_user_role_key(user_id)
        context = self.conversation_context.get(user_role_key, [])
        return {
            "message_count": len(context) - 1 if context else 0,
            "has_context": bool(context),
            "current_role": self.current_role,
            "max_turns": self.max_turns,
            "current_turns": (len(context) - 1) // 2 if context else 0
        }

    async def close(self) -> None:
        """关闭客户端"""
        if self._client:
            await self._client.close()
