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
        执行文本合成并返回结果
        Returns:
            {
                "success": bool,
                "audio_data": bytes,  # PCM音频数据
                "raw_response": Dict[str, Any]  # 原始响应
            }
        """
        pass

    @abstractmethod
    async def synthesize_stream(self, text_chunks: AsyncGenerator[str, None]) -> AsyncGenerator[Dict[str, Any], None]:
        """
        流式文本合成
        Args:
            text_chunks: 文本块的异步生成器
        Yields:
            {
                "success": bool,
                "chunk": bytes,  # PCM音频数据块
                "type": str     # "audio_chunk" 或 "done"
            }
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """释放引擎资源"""
        pass