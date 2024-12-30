import time
from fastapi import FastAPI, Request, WebSocket, Depends

import sys
sys.path.append("/home/wds/workspace/now/LLM_router")

from app.middlewares.auth_middleware import AuthMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.utils.permission_checker import check_permission
from app.routers.websocket_handler import handle_websocket_connection   # 导入 WebSocket 处理函数
import logging
logger = logging.getLogger(__name__)

app = FastAPI()

# 添加中间件
app.add_middleware(LoggingMiddleware)  # 日志中间件
# app.add_middleware(AuthMiddleware)     # 鉴权中间件,仅判断是否有权限

auth_middleware = AuthMiddleware(app=app)

# 使用 WebSocket 路由
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 调用 websocket_auth 方法进行鉴权
    if not await auth_middleware.websocket_auth(websocket):
        return  # 鉴权失败，连接已关闭

    # 鉴权成功，继续处理 WebSocket 连接
    await handle_websocket_connection(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

