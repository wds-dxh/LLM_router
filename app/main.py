from fastapi import FastAPI, Request, WebSocket

import sys
sys.path.append("/home/wds/workspace/now/LLM_router")

from app.middlewares.auth_middleware import AuthMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.utils.permission_checker import check_permission
from app.routers import websocket   # 导入 WebSocket 路由

app = FastAPI()

# 添加中间件
app.add_middleware(LoggingMiddleware)  # 日志中间件
app.add_middleware(AuthMiddleware)     # 鉴权中间件,仅判断是否有权限

# 添加 WebSocket 路由
app.include_router(websocket.router)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

