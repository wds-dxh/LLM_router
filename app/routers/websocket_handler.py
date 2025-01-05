import asyncio
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


class WebSocketConnectionContext:
    def __init__(self):
        self.shared_audio_buffer = bytearray()
        self.can_send_audio = False


async def audio_sender(websocket: WebSocket, context: WebSocketConnectionContext):
    """
    异步发送音频数据，带流控制
    """
    try:
        while True:
            if context.can_send_audio and len(context.shared_audio_buffer) >= BUFFER_SIZE:
                chunk = context.shared_audio_buffer[:BUFFER_SIZE]
                context.shared_audio_buffer = context.shared_audio_buffer[BUFFER_SIZE:]
                await websocket.send_bytes(chunk)
                context.can_send_audio = False  # 发送完一包后停止发送
            else:
                await asyncio.sleep(0.06)
    except asyncio.CancelledError:
        logger.info("Audio sender task was cancelled")
    except Exception as e:
        logger.error(f"Audio sender error: {str(e)}")


async def handle_websocket_connection(websocket: WebSocket):
    """
    处理 WebSocket 连接，逐句发送响应
    """
    context = WebSocketConnectionContext()
    send_task = None  # 用于管理音频发送任务

    try:
        auth = getattr(websocket.state, "auth", None)
        accumulated_text = ""  # 用于累积返回的文本

        # 启动音频发送任务, 用于异步发送音频数据
        send_task = asyncio.create_task(audio_sender(websocket, context))

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            print(message)

            if 'role' in message:
                llm_service.set_role(message['role'])

            if 'text' in message and message['text'] != "ok" and message['text'] != "exit":
                async for chunk in llm_service.chat_stream(auth.get("device_id", set()), message['text']):
                    if chunk.get('type') == 'content':
                        accumulated_text += chunk['text']

                        if any(accumulated_text.endswith(suffix) for suffix in ['。', '！', '!', '.', '？', '?', '；', ';']):
                            index = max(accumulated_text.rfind(suffix) for suffix in [
                                        '。', '！', '!', '.', '？', '?', '；', ';'])
                            sentence = accumulated_text[:index + 1]
                            print("sentence:", sentence)

                            # 生成音频数据
                            audio_data = await tts_service.synthesize(sentence)
                            context.can_send_audio = True  # 当收到一次数据的时候也要触发一下发送任务

                            context.shared_audio_buffer.extend(
                                audio_data['audio_data'])
                            accumulated_text = accumulated_text[index + 1:]

            if message['text'] == "ok":
                context.can_send_audio = True  # 收到ok消息时允许发送下一包数据
            if message['text'] == "exit":
                context.can_send_audio = False  # 收到exit消息时停止发送数据
                if send_task and not send_task.done():
                    # 数据清空
                    context.shared_audio_buffer.clear()

    except WebSocketDisconnect as e:
        logger.info(f"WebSocket connection closed: {e.code}, {e.reason}")
    except Exception as e:
        logger.error(f"WebSocket connection error: {str(e)}")
    finally:
        logger.info("WebSocket connection handler has exited")
        # 在断开连接时取消发送任务
        if send_task and not send_task.done():
            send_task.cancel()
        context.can_send_audio = False  # 重置流控制变量
