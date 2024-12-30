import os
import time
import json
import base64
import hashlib
import hmac
import ssl
import websocket
import httpx
from datetime import datetime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from typing import Dict, Any, AsyncGenerator, Tuple
from time import mktime
from threading import Thread
from queue import Queue, Empty
from .base import BaseTTSEngine

# Status flags for streaming
STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

class IflytekEngine(BaseTTSEngine):
    """科大讯飞TTS引擎实现"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._send_queue = Queue()  # Queue for sending text chunks
        self._ws_buffer = []        # Buffer to store received audio chunks

    def _validate_config(self) -> None:
        required = ["app_id", "api_key", "api_secret"]
        for r in required:
            if r not in self.config:
                raise ValueError(f"Missing {r} in Iflytek TTS config")

    def _prepare_ws_url(self) -> str:
        """
        根据 app_id, api_key, api_secret 生成 TTS WebSocket 鉴权 URL
        """
        base_url = "wss://tts-api.xfyun.cn/v2/tts"

        # 获取当前 RFC1123 格式时间
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 计算签名
        signature_origin = f"host: ws-api.xfyun.cn\n"
        signature_origin += f"date: {date}\n"
        signature_origin += "GET /v2/tts HTTP/1.1"
        signature_sha = hmac.new(
            self.config["api_secret"].encode("utf-8"),
            signature_origin.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode("utf-8")

        # 生成 authorization
        authorization_origin = (
            f'api_key="{self.config["api_key"]}", '
            f'algorithm="hmac-sha256", '
            f'headers="host date request-line", '
            f'signature="{signature_sha}"'
        )
        authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode("utf-8")

        # 拼接鉴权参数
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn",
        }

        return base_url + "?" + urlencode(v)

    def _get_business_args(self) -> Dict[str, Any]:
        """
        获取业务参数，避免在多个方法中重复定义
        """
        return {
            "aue": self.config.get("aue", "raw"),
            "auf": self.config.get("auf", "audio/L16;rate=16000"),
            "vcn": self.config.get("vcn", "x_yuer"),
            "tte": self.config.get("tte", "utf8"),
            "speed": self.config.get("speed", 50),
            "pitch": self.config.get("pitch", 50),
            "volume": self.config.get("volume", 50)
        }

    def _send_frame(self, ws, text_piece: str, status: int):
        """发送一次数据帧"""
        if text_piece:
            encoded_text = base64.b64encode(text_piece.encode("utf-8")).decode("utf-8")
        else:
            encoded_text = ""

        data = {
            "status": status,
            "text": encoded_text
        }
        d = {
            "common": {"app_id": self.config["app_id"]},
            "business": self._get_business_args(),
            "data": data
        }
        ws.send(json.dumps(d))

    def _on_message(self, ws, message):
        """严格按您给的示例解析数据"""
        try:
            msg_data = json.loads(message)
            code = msg_data["code"]
            sid = msg_data["sid"]
            audio = base64.b64decode(msg_data["data"]["audio"])
            print("receive msg")
            status = msg_data["data"]["status"]
            print(status)
            if status == 2:
                print("ws is closed")
                ws.close()
            if code != 0:
                errMsg = msg_data["message"]
                print(f"sid:{sid} call error:{errMsg} code is:{code}")
            else:
                # 同时保存在 self._ws_buffer 中
                self._ws_buffer.append(audio)
                print("receive audio")
        except Exception as e:
            print("receive msg, but parse exception:", e)

    def _on_error(self, ws, error):
        print("TTS WebSocket error:", error)

    def _on_close(self, ws, close_status_code, close_msg):
        print("TTS WebSocket closed.")

    def _on_open(self, ws):
        """
        发送文本数据帧的线程函数
        """
        def run():
            while True:
                try:
                    item = self._send_queue.get()
                    if item is None:
                        # Sentinel received, close the WebSocket
                        ws.close()
                        break
                    text, status = item
                    self._send_frame(ws, text, status)
                except Exception as e:
                    print("Exception in _on_open run:", e)
                    ws.close()
                    break

        thread = Thread(target=run)
        thread.start()

    async def synthesize(self, text: str) -> Dict[str, Any]:
        """
        一次性合成: 不保存文件, 直接返回PCM数据
        """
        # 使用流式合成并收集所有PCM数据
        async for audio_chunk in self.synthesize_stream(iter([(text, True), ("", False)])):
            if audio_chunk["type"] == "audio_chunk":
                # Collect audio data
                if "audio_data" not in locals():
                    audio_data = bytearray()
                audio_data += audio_chunk["chunk"]
            elif audio_chunk["type"] == "done":
                break
        return {
            "success": True,
            "audio_data": bytes(audio_data) if 'audio_data' in locals() else b"",
            "raw_response": {"mock": "data"}
        }

    async def synthesize_stream(self, text_chunks: AsyncGenerator[Tuple[str, bool], None]) -> AsyncGenerator[Dict[str, Any], None]:
        """
        流式合成: 发送文本块并实时返回音频块
        Args:
            text_chunks: 异步生成器，生成 (text, is_continue) 元组
                text: 文本块
                is_continue: 是否继续发送，False 表示结束
        """
        self._ws_buffer = []
        self._send_queue = Queue()

        ws_url = self._prepare_ws_url()
        ws = websocket.WebSocketApp(
            ws_url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )

        # Start WebSocket in a separate thread
        ws_thread = Thread(target=ws.run_forever, kwargs={"sslopt": {"cert_reqs": ssl.CERT_NONE}})
        ws_thread.start()

        # Wait for the connection to establish
        time.sleep(1)

        # Send text chunks with appropriate status
        first = True
        try:
            async for chunk, is_continue in text_chunks:
                if first:
                    status = STATUS_FIRST_FRAME
                    first = False
                elif is_continue:
                    status = STATUS_CONTINUE_FRAME
                else:
                    status = STATUS_LAST_FRAME
                self._send_queue.put((chunk, status))
                if not is_continue:
                    break
        except Exception as e:
            print("Error while sending text chunks:", e)
        finally:
            # Ensure the WebSocket is closed
            self._send_queue.put((None, STATUS_LAST_FRAME))

        # Wait for the WebSocket thread to finish
        ws_thread.join()

        # Yield audio chunks as they are received
        while self._ws_buffer:
            chunk = self._ws_buffer.pop(0)
            yield {
                "success": True,
                "chunk": chunk,
                "type": "audio_chunk"
            }

        # Indicate that synthesis is done
        yield {"success": True, "chunk": b"", "type": "done"}

    async def close(self) -> None:
        """关闭连接等资源"""
        # Send sentinel to close the WebSocket connection if it's still open
        self._send_queue.put(None)
        # Additional cleanup can be performed here if necessary
        pass
