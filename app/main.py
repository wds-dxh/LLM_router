from fastapi import FastAPI
from fastapi.websockets import WebSocket
from routers.websocket_handler import websocket_handler
import json
import os

# 加载配置
config_path = os.path.join(os.path.dirname(__file__), "config/config.json")
with open(config_path, "r") as f:
    config = json.load(f)

# 初始化 FastAPI 应用
app = FastAPI()

# 使用 WebSocket 路由
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_handler(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config["host"], port=config["port"])
