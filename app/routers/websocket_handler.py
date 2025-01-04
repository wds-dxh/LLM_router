import asyncio
import time
import json
import logging
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
from app.utils.config_loader import ConfigLoader
from app.services.llm_service import LLMService
from app.services.tts_service import TTSService

logger = logging.getLogger(__name__)

config_loader = ConfigLoader()
# 创建 LLMService 实例
llm_service = LLMService(config_loader)
tts_service = TTSService()

# 定义缓冲区大小，每次读取1024采样点，每个采样点占2字节
BUFFER_SIZE = 1024 * 2 * 4

# 全局音频缓冲区
shared_audio_buffer = bytearray()


async def audio_sender(websocket: WebSocket):
    """
    异步发送音频数据
    """
    global shared_audio_buffer
    try:
        while True:
            if len(shared_audio_buffer) >= BUFFER_SIZE:
                chunk = shared_audio_buffer[:BUFFER_SIZE]
                shared_audio_buffer = shared_audio_buffer[BUFFER_SIZE:]
                await websocket.send_bytes(chunk)
                await asyncio.sleep(0.067)  # 每次发送后延迟10ms

            else:
                await asyncio.sleep(0.06)  # 如果没有数据，短暂等待
    except Exception as e:
        logger.error(f"Audio sender error: {str(e)}")


async def handle_websocket_connection(websocket: WebSocket):
    """
    处理 WebSocket 连接，逐句发送响应
    """
    global shared_audio_buffer
    try:
        auth = getattr(websocket.state, "auth", None)
        accumulated_text = ""  # 用于累积返回的文本

        # 启动音频发送任务, 用于异步发送音频数据
        send_task = asyncio.create_task(audio_sender(websocket))

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            print(message)

            if 'role' in message:
                llm_service.set_role(message['role'])

            if 'text' in message:
                async for chunk in llm_service.chat_stream(auth.get("device_id", set()), message['text']):
                    if chunk.get('type') == 'content':
                        accumulated_text += chunk['text']

                        if any(accumulated_text.endswith(suffix) for suffix in ['。', '！', '!', '.', '？', '?', '；', ';']):
                            index = max(accumulated_text.rfind(suffix) for suffix in [
                                        '。', '！', '!', '.', '？', '?', '；', ';'])
                            sentence = accumulated_text[:index + 1]
                            print("sentence:", sentence)

                            # 生成音频数据
                            # audio_data = await tts_service.synthesize(sentence)
                            # shared_audio_buffer.extend(
                            #     audio_data['audio_data'])

                            # # 从文件中读取音频数据
                            filename = f"audio_output1.pcm"
                            with open(filename, "rb") as f:
                                audio_data = f.read()
                            shared_audio_buffer.extend(audio_data)

                            # 一次性发送音频数据
                            # await websocket.send_bytes(audio_data['audio_data'])
                            accumulated_text = accumulated_text[index + 1:]

    except WebSocketDisconnect as e:
        logger.info(f"WebSocket connection closed: {e.code}, {e.reason}")
    except Exception as e:
        logger.error(f"WebSocket connection error: {str(e)}")
        await websocket.close()
    finally:
        logger.info("WebSocket connection handler has exited")
