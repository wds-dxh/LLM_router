from typing import Dict, Any
from .base import BaseLLMEngine
from .openai import OpenAIEngine
from .ollama import OllamaEngine

class LLMEngineFactory:
    """LLM引擎工厂类"""
    
    _engines = {
        "openai": OpenAIEngine,
        "ollama": OllamaEngine  # 添加ollama支持
    }

    @classmethod
    def create(cls, provider: str, config: Dict[str, Any]) -> BaseLLMEngine:
        """创建LLM引擎实例"""
        if provider not in cls._engines:
            raise ValueError(f"Unsupported LLM provider: {provider}")
            
        engine_class = cls._engines[provider]
        return engine_class(config)
