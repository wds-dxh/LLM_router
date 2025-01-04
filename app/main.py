import logging
from app.routers.llm import router as llm_router
from app.routers.websocket_handler import handle_websocket_connection   # 导入 WebSocket 处理函数
from app.utils.permission_checker import check_permission
from app.middlewares.logging_middleware import LoggingMiddleware
from app.middlewares.auth_middleware import AuthMiddleware
import time
from fastapi import FastAPI, Request, WebSocket, Depends
from fastapi.staticfiles import StaticFiles
from app.routers.llmstatic import router as llmstatic_router

import sys
sys.path.append("/home/wds/workspace/now/LLM_router")


logger = logging.getLogger(__name__)

app = FastAPI()

# 添加中间件
app.add_middleware(LoggingMiddleware)  # 日志中间件
# app.add_middleware(AuthMiddleware)     # 鉴权中间件,仅判断是否有权限

auth_middleware = AuthMiddleware(app=app)

# 添加静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册 LLM 路由
app.include_router(llm_router, prefix="/api/v1")
app.include_router(llmstatic_router, prefix="/api/v1")

# 使用 WebSocket 路由


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 调用 websocket_auth 方法进行鉴权
    if not await auth_middleware.websocket_auth(websocket):
        return  # 鉴权失败，连接已关闭
    # 发送欢迎消息
    # await websocket.send_text("Welcome to WebSocket")

    # 鉴权成功，继续处理 WebSocket 连接
    await handle_websocket_connection(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# 启动
# gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --workers 10
