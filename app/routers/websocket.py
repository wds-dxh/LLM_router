from fastapi import APIRouter, WebSocket, Depends, HTTPException
from starlette.websockets import WebSocketDisconnect
from app.middlewares.auth_middleware import AuthMiddleware

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, auth: dict = Depends(AuthMiddleware)):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # 处理接收到的数据
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
    except HTTPException as e:
        await websocket.close(code=e.status_code)
        print(f"WebSocket connection closed with code: {e.status_code}")



