import asyncio
from typing import Optional, Callable, Dict, Any, AsyncGenerator
from inspect import iscoroutinefunction
from app.services.tts_engine.factory import TTSEngineFactory
from app.services.tts_engine.base import BaseTTSEngine
from app.utils.config_loader import ConfigLoader
# ...existing imports...

class TTSService:
    """TTS服务类"""

    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader
        self._engine: Optional[BaseTTSEngine] = None
        self._callback: Optional[Callable] = None
        self._initialize_default_engine()

    async def __aenter__(self):
        """支持异步上下文管理器"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self._engine, 'close'):
            await self._engine.close()

    def _initialize_default_engine(self) -> None:
        """初始化默认引擎"""
        tts_config = self.config_loader.get_tts_config()  # 需要在 config_loader 里添加 get_tts_config()
        if not tts_config:
            raise RuntimeError("TTS configuration not found")

        default_provider = tts_config.get("default_provider")
        if not default_provider:
            raise ValueError("No default TTS provider specified")

        # 获取合成配置
        provider_config = self.config_loader.get_provider_config("tts", default_provider)
        self._engine = TTSEngineFactory.create(default_provider, provider_config)

    def set_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """设置回调函数"""
        self._callback = callback

    async def synthesize(self, text: str) -> Dict[str, Any]:
        """执行一次性合成"""
        if not self._engine:
            raise RuntimeError("TTS engine not initialized")

        try:
            result = await self._engine.synthesize(text)
            if self._callback:
                # 区分同步/异步回调
                if iscoroutinefunction(self._callback):
                    await self._callback(result)
                else:
                    self._callback(result)
            return result
        except Exception as e:
            raise RuntimeError(f"Error during TTS synthesis: {str(e)}")

    async def synthesize_stream(self, text: str) -> AsyncGenerator[Dict[str, Any], None]:
        """流式合成"""
        if not self._engine:
            raise RuntimeError("TTS engine not initialized")

        try:
            async for chunk in self._engine.synthesize_stream(text):
                if self._callback:
                    if iscoroutinefunction(self._callback):
                        await self._callback(chunk)
                    else:
                        self._callback(chunk)
                yield chunk
        except Exception as e:
            raise RuntimeError(f"Error during streaming TTS: {str(e)}")

    async def synthesize_stream(self, text_chunks: AsyncGenerator[str, None]) -> AsyncGenerator[Dict[str, Any], None]:
        """
        流式合成: 按段获取文本并逐步生成音频流
        text_chunks: 异步生成器，一次返回一小段文本
        """
        if not self._engine:
            raise RuntimeError("TTS engine not initialized")

        try:
            # 直接将 text_chunks 传给引擎
            async for audio_chunk in self._engine.synthesize_stream(text_chunks):
                # 每次返回已合成的PCM数据片段
                if self._callback:
                    if iscoroutinefunction(self._callback):
                        await self._callback(audio_chunk)
                    else:
                        self._callback(audio_chunk)
                yield audio_chunk
        except Exception as e:
            raise RuntimeError(f"Error during streaming TTS: {str(e)}")

    async def switch_engine(self, provider: str) -> None:
        """切换TTS引擎"""
        if hasattr(self._engine, 'close'):
            await self._engine.close()

        provider_config = self.config_loader.get_provider_config("tts", provider)
        self._engine = TTSEngineFactory.create(provider, provider_config)

