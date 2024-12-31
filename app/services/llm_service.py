from typing import Optional, Callable, Dict, Any, AsyncGenerator, List
from .llm_engine.factory import LLMEngineFactory
from .llm_engine.base import BaseLLMEngine
from ..utils.config_loader import ConfigLoader


class LLMService:
    """LLM服务类"""

    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader
        self._engine: Optional[BaseLLMEngine] = None    # 定义一个可选的引擎对象
        self._callback: Optional[Callable] = None
        self._initialize_default_engine()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self._engine, 'close'):
            await self._engine.close()

    def _initialize_default_engine(self):
        """初始化默认引擎"""
        llm_config = self.config_loader.get_llm_config()
        if not llm_config:
            raise RuntimeError("LLM configuration not found")

        default_provider = llm_config.get("default_provider")
        if not default_provider:
            raise ValueError("No default provider specified in LLM config")

        # 获取provider配置，这里会自动合并storage等公共配置
        provider_config = self.config_loader.get_provider_config(
            "llm", default_provider)
        self._engine = LLMEngineFactory.create(
            default_provider, provider_config)

    async def switch_engine(self, provider: str) -> None:
        """切换LLM引擎"""
        if hasattr(self._engine, 'close'):
            await self._engine.close()
        provider_config = self.config_loader.get_provider_config(
            "llm", provider)
        self._engine = LLMEngineFactory.create(provider, provider_config)

    def set_role(self, role_type: str) -> bool:
        """设置当前角色"""
        if not self._engine:
            raise RuntimeError("LLM engine not initialized")
        return self._engine.set_role(role_type)

    def get_current_role(self) -> str:
        """获取当前角色"""
        if not self._engine:
            raise RuntimeError("LLM engine not initialized")
        return self._engine.get_current_role()

    def list_available_roles(self) -> List[str]:
        """获取可用角色列表"""
        if not self._engine:
            raise RuntimeError("LLM engine not initialized")
        return self._engine.list_available_roles()

    async def get_conversation_history(self, user_id: str) -> List[Dict]:
        """获取对话历史"""
        if not self._engine:
            raise RuntimeError("LLM engine not initialized")
        return await self._engine.get_conversation_history(user_id)

    def set_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """设置回调函数"""
        self._callback = callback

    async def chat(self, user_id: str, message: str, context: Optional[list] = None) -> Dict[str, Any]:
        """执行对话"""
        if not self._engine:
            raise RuntimeError("LLM engine not initialized")

        try:
            result = await self._engine.chat(user_id, message, context)
            if self._callback:  # 如果有回调函数，执行回调
                await self._callback(result)
            return result
        except Exception as e:
            print(f"Error during chat: {str(e)}")
            raise

    async def chat_stream(self, user_id: str, message: str, context: Optional[list] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """流式对话"""
        if not self._engine:
            raise RuntimeError("LLM engine not initialized")
        assistant_response_buffer = ""
        try:
            async for chunk in self._engine.chat_stream(user_id, message, context):
                assistant_response_buffer += chunk['text']
                yield chunk
        except Exception as e:
            print(f"Error during stream chat: {str(e)}")
            raise
        if self._callback:  # 使用完整的接收到的响应调用回调
            await self._callback(assistant_response_buffer)

    def clear_context(self, user_id: str) -> None:
        """清除用户上下文"""
        if not self._engine:
            raise RuntimeError("LLM engine not initialized")
        self._engine.clear_context(user_id)

    def get_context_summary(self, user_id: str) -> Dict[str, Any]:
        """获取上下文摘要"""
        if not self._engine:
            raise RuntimeError("LLM engine not initialized")
        return self._engine.get_context_summary(user_id)
