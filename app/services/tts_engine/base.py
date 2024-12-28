
from abc import ABC, abstractmethod
from typing import Dict, Any, AsyncGenerator

class BaseTTSEngine(ABC):
    """TTS引擎基类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._validate_config()

    @abstractmethod
    def _validate_config(self) -> None:
        """验证配置"""
        pass

    @abstractmethod
    async def synthesize(self, text: str) -> Dict[str, Any]:
        """
        执行文本合成并返回结果，例如:
        { 
            "success": True, 
            "audio_data": b"...", 
            "raw_response": {...} 
        }
        """
        pass

    @abstractmethod
    async def synthesize_stream(self, text: str) -> AsyncGenerator[Dict[str, Any], None]:
        """流式文本合成"""
        pass

    @abstractmethod
    async def close(self) -> None:
        """释放引擎资源（如连接）"""
        pass