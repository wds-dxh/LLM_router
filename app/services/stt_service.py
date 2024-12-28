from typing import Optional, Callable, Dict, Any
from app.services.stt_engine.factory import STTEngineFactory
from app.services.stt_engine.base import BaseSTTEngine
from app.utils.config_loader import ConfigLoader
# 建议使用 Python logging 或 FastAPI 自带的 logger，而不是 print()
from app.utils.logger import get_logger

logger = get_logger(__name__)


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
            logger.debug("STT engine client closed.")

    def _initialize_default_engine(self):
        """初始化默认引擎"""
        stt_config = self.config_loader.get_stt_config()
        default_provider = stt_config.get("default_provider")
        provider_config = self.config_loader.get_provider_config("stt", default_provider)   
        self._engine = STTEngineFactory.create(default_provider, provider_config)
        logger.debug(f"Initialized default STT engine: {default_provider}")

    def set_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """
        设置回调函数。  
        如果回调是异步函数，需要在调用处使用 `await self._callback(result)`；  
        如果回调是同步函数，可在这里做一层判断或转换。  
        """
        self._callback = callback
        logger.debug("Callback function set for STTService.")

    async def recognize(self, audio_data: bytes, **kwargs) -> Dict[str, Any]:
        """执行语音识别"""
        if not self._engine:
            raise RuntimeError("STT engine not initialized")

        try:
            result = await self._engine.recognize(audio_data, **kwargs)
            # 获取最终文本
            final_text = result.get('text', '')
            # 回调只传入完整文本即可
            if self._callback:
                await self._callback({"final_text": final_text})
            return result
        except Exception as e:
            # 建议使用 logger 代替 print
            logger.error(f"Error during recognition: {e}", exc_info=True)
            # 保持向上抛出以便上层处理
            raise

    async def recognize_stream(self, audio_stream, **kwargs):
        """流式语音识别"""
        if not self._engine:
            raise RuntimeError("STT engine not initialized")

        accumulated_text = ""
        try:
            async for partial_result in self._engine.recognize_stream(audio_stream, **kwargs):
                # 这里 partial_result 可能是多次返回的文本片段
                accumulated_text += partial_result.get('text', "")
            # 全部识别结束后再一次性回调
            if self._callback:
                await self._callback({"final_text": accumulated_text})
            # 同时可将最终结果返回给调用者
            return {"text": accumulated_text}
        except Exception as e:
            logger.error(f"Error during streaming recognition: {e}", exc_info=True)
            raise

    async def switch_engine(self, provider: str):
        """
        切换STT引擎。  
        如果需要先关闭旧引擎，可以在此处处理。例如：  
        
            if hasattr(self._engine, 'close'):
                await self._engine.close()
        
        然后再创建新的引擎实例。
        """
        provider_config = self.config_loader.get_provider_config("stt", provider)
        
        # 如果需要先释放旧的资源，可以在这里做
        if hasattr(self._engine, 'close'):
            await self._engine.close()
            logger.debug(f"Closed existing STT engine before switching to {provider}.")
        
        self._engine = STTEngineFactory.create(provider, provider_config)
        logger.debug(f"Switched STT engine to: {provider}")
