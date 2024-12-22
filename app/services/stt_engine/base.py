from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseSTTEngine(ABC):
    """STT引擎基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._validate_config()

    @abstractmethod
    def _validate_config(self) -> None:
        """验证配置"""
        pass

    @abstractmethod
    async def recognize(self, audio_data: bytes, **kwargs) -> Dict[str, Any]:
        """
        执行语音识别
        返回格式: {
            'text': str,              # 识别文本
            'confidence': float,      # 置信度
            'duration': float,        # 音频时长
            'raw_response': dict      # 原始响应
        }
        """
        pass

    @abstractmethod
    async def recognize_stream(self, audio_stream, **kwargs):
        """流式语音识别"""
        pass
