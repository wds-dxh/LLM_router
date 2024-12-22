from typing import Dict, Any
from .base import BaseSTTEngine
from .aliyun import AliyunSTTEngine

class STTEngineFactory:
    """STT引擎工厂类"""
    
    _engines = {
        "aliyun": AliyunSTTEngine,
        # 后续可以添加更多引擎
    }

    @classmethod
    def create(cls, provider: str, config: Dict[str, Any]) -> BaseSTTEngine:
        """创建STT引擎实例"""
        if provider not in cls._engines:
            raise ValueError(f"Unsupported STT provider: {provider}")
            
        engine_class = cls._engines[provider]
        return engine_class(config)
