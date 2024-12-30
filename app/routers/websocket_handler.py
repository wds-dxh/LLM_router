import time
import json
import logging
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
from app.utils.config_loader import ConfigLoader
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

config_loader = ConfigLoader()
# 创建 LLMService 实例
llm_service = LLMService(config_loader)
async def handle_websocket_connection(websocket: WebSocket):
    """
    处理 WebSocket 连接
    """
    try:
        auth = getattr(websocket.state, "auth", None)
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            message = json.loads(data)

            if 'role' in message:
                llm_service.set_role(message['role'])
                    # await websocket.send_text(f"角色已切换为: {llm_service.get_current_role()}")

            # if 'text' in message:
            #     response = await llm_service.chat(auth.get("device_id", set()), message['text'])
            #     await websocket.send_text(f"响应: {response['text']}")
                
            if 'text' in message:
            
                async for chunk in llm_service.chat_stream(auth.get("device_id", set()), message['text']):
                    if chunk.get('type') == 'content':
                        await websocket.send_text(chunk['text'])

    except WebSocketDisconnect as e:
        logger.info(f"WebSocket connection closed: {e.code}, {e.reason}")
    except Exception as e:
        logger.error(f"WebSocket connection error: {str(e)}")
        await websocket.close()
    finally:
        logger.info("WebSocket connection handler has exited")
        del websocket


