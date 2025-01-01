import uuid
import base64
import httpx
import json
from typing import AsyncGenerator, Dict, Any, ClassVar, Optional
from .base import BaseTTSEngine


class VolcanoTTSEngine(BaseTTSEngine):
    """火山TTS引擎实现"""
    _client: ClassVar[Optional[httpx.AsyncClient]] = None

    def _validate_config(self) -> None:
        required_fields = ["appid", "access_token", "cluster", "host"]
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"Missing required config field: {field}")

        self._init_client()
        self.api_url = f"https://{self.config['host']}/api/v1/tts"
        # 修改认证头格式
        self.headers = {
            "Authorization": f"Bearer;{self.config['access_token']}",
            "Content-Type": "application/json"
        }

    def _init_client(self) -> None:
        """初始化HTTP客户端"""
        if self._client is None:
            pool_config = self.config.get("connection_pool", {})
            limits = httpx.Limits(
                max_connections=pool_config.get("max_connections", 4),
                max_keepalive_connections=pool_config.get(
                    "max_keepalive", 1000),
                keepalive_expiry=pool_config.get("keepalive_expiry", 30.0)
            )

            timeout = httpx.Timeout(pool_config.get("timeout", 30.0))
            self.__class__._client = httpx.AsyncClient(
                timeout=timeout,
                limits=limits
            )

    async def synthesize(self, text: str) -> Dict[str, Any]:
        request_data = self._build_request(text)
        try:
            # 使用json.dumps确保正确的序列化
            response = await self._client.post(
                self.api_url,
                content=json.dumps(request_data),
                headers=self.headers
            )
            response.raise_for_status()
            result = response.json()

            if "data" not in result:
                return {"success": False, "error": "No data in response"}

            audio_data = base64.b64decode(result["data"])
            return {
                "success": True,
                "audio_data": audio_data,
                "raw_response": result
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def synthesize_stream(self, text_chunks: AsyncGenerator[str, None]) -> AsyncGenerator[Dict[str, Any], None]:
        async for text in text_chunks:
            result = await self.synthesize(text)
            if result["success"]:
                yield {
                    "success": True,
                    "chunk": result["audio_data"],
                    "type": "audio_chunk"
                }
        yield {"success": True, "type": "done"}

    def _build_request(self, text: str) -> Dict:
        # 严格按照示例代码构建请求
        return {
            "app": {
                "appid": self.config["appid"],
                "token": "access_token",  # 保持这个值不变
                "cluster": self.config["cluster"]
            },
            "user": {
                "uid": str(uuid.uuid4())  # 每次请求生成新的uid
            },
            "audio": {
                "voice_type": self.config.get("voice_type", "BV700_streaming"),
                "encoding": "mp3",
                "speed_ratio": self.config.get("audio_config", {}).get("speed_ratio", 1.0),
                "volume_ratio": self.config.get("audio_config", {}).get("volume_ratio", 1.0),
                "pitch_ratio": self.config.get("audio_config", {}).get("pitch_ratio", 1.0)
            },
            "request": {
                "reqid": str(uuid.uuid4()),
                "text": text,
                "text_type": "plain",
                "operation": "query",
                "with_frontend": 1,
                "frontend_type": "unitTson"
            }
        }

    @classmethod
    async def close(cls) -> None:
        """关闭共享的HTTP客户端"""
        if cls._client is not None:
            await cls._client.aclose()
            cls._client = None
