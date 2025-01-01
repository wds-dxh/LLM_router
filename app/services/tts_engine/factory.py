from typing import Dict, Any
from .base import BaseTTSEngine
from .volcano import VolcanoTTSEngine


class TTSEngineFactory:
    """TTS引擎工厂类"""

    _engines = {
        "volcano": VolcanoTTSEngine,
        # ...可以扩展更多TTS引擎
    }

    @classmethod
    def create(cls, provider: str, config: Dict[str, Any]) -> BaseTTSEngine:
        if provider not in cls._engines:
            raise ValueError(f"Unsupported TTS provider: {provider}")
        engine_class = cls._engines[provider]
        return engine_class(config)
