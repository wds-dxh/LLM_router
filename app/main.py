from fastapi import FastAPI, Request
from app.middlewares.auth_middleware import AuthMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.utils.permission_checker import check_permission

app = FastAPI()

# 添加中间件
app.add_middleware(LoggingMiddleware)  # 日志中间件
app.add_middleware(AuthMiddleware)     # 鉴权中间件

# 基础测试路由 - 只测试鉴权中间件
@app.get("/test")
async def test_endpoint(request: Request):
    auth_info = request.state.auth
    return {
        "message": "鉴权成功",
        "auth_info": {
            "api_key": auth_info["api_key"],
            "permissions": list(auth_info["permissions"])
        }
    }

# 需要 read 权限的路由
@app.get("/test/llm")
@check_permission("llm.chat")
async def test_read(request: Request):
    return {"message": "成功访问只读资源"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
