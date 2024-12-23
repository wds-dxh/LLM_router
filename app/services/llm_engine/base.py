from abc import ABC, abstractmethod
from typing import Dict, Any, AsyncGenerator, Optional, List

class BaseLLMEngine(ABC):
    """LLM引擎基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._validate_config()
        self.current_role = "default"

    @abstractmethod
    def _validate_config(self) -> None:
        """验证配置"""
        pass

    @abstractmethod
    async def chat(self, user_id: str, message: str, context: Optional[list] = None) -> Dict[str, Any]:
        """执行对话"""
        pass

    @abstractmethod
    async def chat_stream(self, user_id: str, message: str, context: Optional[list] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """流式对话"""
        pass

    @abstractmethod
    def set_role(self, role_type: str) -> bool:
        """设置当前角色"""
        pass

    @abstractmethod
    def get_current_role(self) -> str:
        """获取当前角色"""
        pass

    @abstractmethod
    def list_available_roles(self) -> List[str]:
        """获取可用角色列表"""
        pass

    @abstractmethod
    async def save_conversation(self, user_id: str, conversation: List[Dict]) -> None:
        """保存对话历史"""
        pass

    @abstractmethod
    async def get_conversation_history(self, user_id: str) -> List[Dict]:
        """获取对话历史"""
        pass

    @abstractmethod
    async def close(self) -> None:
        """关闭引擎资源"""
        pass
