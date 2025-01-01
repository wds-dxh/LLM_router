from typing import Dict, Any, Optional
from app.utils.config_loader import ConfigLoader
from .tts_engine.factory import TTSEngineFactory
from .tts_engine.base import BaseTTSEngine


class TTSService:
    """TTS服务管理类"""

    def __init__(self):
        self.config_loader = ConfigLoader()
        self.tts_config = self.config_loader.get_tts_config()
        self.default_provider = self.tts_config["default_provider"]
        self._engines: Dict[str, BaseTTSEngine] = {}

    def _get_engine(self, provider: Optional[str] = None) -> BaseTTSEngine:
        """获取TTS引擎实例"""
        provider = provider or self.default_provider

        if provider not in self._engines:
            provider_config = self.tts_config["providers"].get(provider)
            if not provider_config:
                raise ValueError(f"Provider {provider} not found in config")
            self._engines[provider] = TTSEngineFactory.create(
                provider, provider_config)

        return self._engines[provider]

    async def synthesize(self, text: str, provider: Optional[str] = None) -> Dict[str, Any]:
        """
        执行文本到语音转换
        Args:
            text: 要转换的文本
            provider: TTS提供商，如果为None则使用默认提供商
        Returns:
            转换结果
        """
        engine = self._get_engine(provider)
        return await engine.synthesize(text)

    async def close(self) -> None:
        """关闭所有TTS引擎"""
        for engine in self._engines.values():
            await engine.close()
        self._engines.clear()

    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()
