from typing import Optional, Callable, Dict, Any
from app.services.stt_engine.factory import STTEngineFactory
from app.services.stt_engine.base import BaseSTTEngine
from app.utils.config_loader import ConfigLoader

class STTService:
    """STT服务类"""
    
    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader
        self._engine: Optional[BaseSTTEngine] = None
        self._callback: Optional[Callable] = None
        self._initialize_default_engine()

    async def __aenter__(self):
        """支持异步上下文管理器"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """确保引擎资源正确释放"""
        if hasattr(self._engine, 'close'):
            await self._engine.close()

    def _initialize_default_engine(self):
        """初始化默认引擎"""
        stt_config = self.config_loader.get_stt_config()
        default_provider = stt_config.get("default_provider")
        provider_config = self.config_loader.get_provider_config("stt", default_provider)
        self._engine = STTEngineFactory.create(default_provider, provider_config)

    def set_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """设置回调函数"""
        self._callback = callback

    async def recognize(self, audio_data: bytes, **kwargs) -> Dict[str, Any]:
        """执行语音识别"""
        if not self._engine:
            raise RuntimeError("STT engine not initialized")

        try:
            result = await self._engine.recognize(audio_data, **kwargs)
            
            if self._callback:      # 如果设置了回调函数，则执行回调（非常重要！）
                await self._callback(result)
                
            return result
        except Exception as e:
            print(f"Error during recognition: {str(e)}")
            raise

    async def recognize_stream(self, audio_stream, **kwargs):
        """流式语音识别"""
        if not self._engine:
            raise RuntimeError("STT engine not initialized")
            
        async for result in self._engine.recognize_stream(audio_stream, **kwargs):
            if self._callback:
                await self._callback(result)
            yield result

    async def switch_engine(self, provider: str):
        """切换STT引擎"""
        provider_config = self.config_loader.get_provider_config("stt", provider)
        self._engine = STTEngineFactory.create(provider, provider_config)