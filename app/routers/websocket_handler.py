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


async def handle_websocket_connection(websocket: WebSocket):
    """
    处理 WebSocket 连接，逐句发送响应
    """
    try:
        auth = getattr(websocket.state, "auth", None)
        accumulated_text = ""  # 用于累积返回的文本

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            print(message)

            if 'role' in message:
                llm_service.set_role(message['role'])
                # 角色已切换，可以发送一条反馈信息
                # await websocket.send_text(f"角色已切换为: {llm_service.get_current_role()}")

            if 'text' in message:
                async for chunk in llm_service.chat_stream(auth.get("device_id", set()), message['text']):
                    if chunk.get('type') == 'content':
                        accumulated_text += chunk['text']  # 累加文本

                        # 判断文本是否包含结束符，若有，发送之前的文本并保留后续部分
                        # while True:
                        if any(accumulated_text.endswith(suffix) for suffix in ['。', '！', '!', '.', '？', '?', '；', ';']):
                            # 找到结束符，发送前面的文本
                            index = max(accumulated_text.rfind(suffix)
                                        for suffix in ['。', '！', '!', '.', '？', '?', '；', ';'])
                            # 包括结束符
                            sentence = accumulated_text[:index + 1]
                            print("sentence:", sentence)
                            # 生成音频数据
                            audio_data = await tts_service.synthesize(sentence)

                            # 发送完整句子的音频数据
                            await websocket.send_bytes(audio_data['audio_data'])
                            # await websocket.send_text(sentence)

                            # 保留后面的文本，继续累积
                            accumulated_text = accumulated_text[index + 1:]

            # if 'text' in message: # 一次性返回所有文本
            #     accumulated_text = await llm_service.chat(auth.get("device_id", set()), message['text'])
            #     await websocket.send_text(accumulated_text['text'])

    except WebSocketDisconnect as e:
        logger.info(f"WebSocket connection closed: {e.code}, {e.reason}")
    except Exception as e:
        logger.error(f"WebSocket connection error: {str(e)}")
        await websocket.close()
    finally:
        logger.info("WebSocket connection handler has exited")
        del websocket
