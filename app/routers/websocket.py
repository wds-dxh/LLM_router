from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.middlewares.auth_middleware import AuthMiddleware
from app.services.llm_service import LLMService
from app.utils.config_loader import ConfigLoader

router = APIRouter()

async def get_llm_service():
    config_loader = ConfigLoader()
    async with LLMService(config_loader) as llm_service:
        yield llm_service

@router.websocket("/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str, llm_service: LLMService = Depends(get_llm_service)):
    # 鉴权
    api_key_model = AuthMiddleware.api_key_model
    api_key_record = await api_key_model.get_by_device_id(device_id)
    if not api_key_record or api_key_record[4] != 'active':
        await websocket.close(code=1008)
        return

    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"收到消息: {data}")

            # 调用 LLM 服务进行流式响应
            async for chunk in llm_service.chat_stream(device_id, data):
                if chunk.get('type') == 'content':
                    await websocket.send_text(chunk['text'])
    except WebSocketDisconnect:
        print(f"客户端断开连接: {device_id}")
