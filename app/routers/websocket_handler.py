import time
import json
import logging
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
from app.utils.config_loader import ConfigLoader
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

async def handle_websocket_connection(websocket: WebSocket):
    """
    处理 WebSocket 连接
    """
    config_loader = ConfigLoader()
    async with LLMService(config_loader) as llm_service:
        try:
            while True:
                data = await websocket.receive_text()
                print(f"Received: {data}")
                message = json.loads(data)

                if 'role' in message:
                    llm_service.set_role(message['role'])
                    # await websocket.send_text(f"角色已切换为: {llm_service.get_current_role()}")

                if 'text' in message:
                    response = await llm_service.chat("websocket_user", message['text'])
                    await websocket.send_text(f"响应: {response['text']}")
                # 如果关闭了连接，则退出循环
                if websocket.client_state != 1:
                    # 释放llm_service
                    await llm_service.close()
                    break
        except WebSocketDisconnect as e:
            logger.info(f"WebSocket connection closed: {e.code}, {e.reason}")
        except Exception as e:
            logger.error(f"WebSocket connection error: {str(e)}")
            await websocket.close()
        finally:
            logger.info("WebSocket connection handler has exited")



