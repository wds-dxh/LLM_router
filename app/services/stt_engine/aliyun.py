import httpx
from typing import Dict, Any, ClassVar
from .base import BaseSTTEngine

class AliyunSTTEngine(BaseSTTEngine):
    """阿里云STT引擎实现"""
    
    _client: ClassVar[httpx.AsyncClient] = None
    _pool_config: ClassVar[Dict[str, Any]] = None
    
    _default_pool_config = {
        "max_connections": 1,
        "max_keepalive": 1,
        "keepalive_expiry": 30.0
    }
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._format = config.get('format', 'pcm')
        self._sample_rate = config.get('sample_rate', 16000)
        # 更新类的连接池配置
        AliyunSTTEngine._pool_config = config.get('connection_pool', self._default_pool_config)
        self._init_client()

    @classmethod
    def _init_client(cls):
        """初始化共享的HTTP客户端连接池"""
        if cls._client is None:
            pool_config = cls._pool_config or cls._default_pool_config
            print(f"Initializing client with pool config: {pool_config}")  # 用于调试
            
            # 创建限制对象
            limits = httpx.Limits(
                max_connections=pool_config["max_connections"],
                max_keepalive_connections=pool_config["max_keepalive"],
                keepalive_expiry=pool_config["keepalive_expiry"]
            )
            
            # 创建超时对象
            timeout = httpx.Timeout(30.0)
            
            cls._client = httpx.AsyncClient(
                base_url='https://nls-gateway-cn-shanghai.aliyuncs.com',
                timeout=timeout,
                limits=limits
            )

    def _validate_config(self) -> None:
        """验证配置"""
        required_fields = ['app_key', 'token']
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"Missing required field: {field}")

    async def recognize(self, audio_data: bytes, **kwargs) -> Dict[str, Any]:
        """执行语音识别"""
        print("Making request...")  # 添加日志
        request = '/stream/v1/asr'
        request = request + f'?appkey={self.config["app_key"]}'
        request = request + f'&format={self._format}'
        request = request + f'&sample_rate={self._sample_rate}'

        headers = {
            'X-NLS-Token': self.config['token'],
            'Content-type': 'application/octet-stream',
            'Content-Length': str(len(audio_data))
        }
        
        try:
            response = await self._client.post(
                request,
                data=audio_data,
                headers=headers
            )
            response.raise_for_status() # 检查响应状态码
            result = response.json()    # 解析JSON响应
            return self._format_response(result)
        except httpx.HTTPError as e:
            raise RuntimeError(f"HTTP request failed: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to recognize audio: {str(e)}")

    def _format_response(self, raw_response: Dict[str, Any]) -> Dict[str, Any]:
        # return {
        #     'text': raw_response.get('result', ''),
        #     'confidence': raw_response.get('confidence', 0.0),
        #     'duration': raw_response.get('duration', 0.0),
        #     'raw_response': raw_response
        # }
        # 返回格式化后的响应result
        return raw_response.get('result', '')

    async def recognize_stream(self, audio_stream, **kwargs):
        """流式语音识别 - 待实现"""
        raise NotImplementedError("Stream recognition not implemented yet")

    @classmethod
    async def close(cls):
        """关闭共享的客户端连接池"""
        if cls._client:
            await cls._client.aclose()
            cls._client = None
