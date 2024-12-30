import json
import logging
import websocket
import threading

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 LLMService 实例
from app.utils.config_loader import ConfigLoader
from app.services.llm_service import LLMService

config_loader = ConfigLoader()
llm_service = LLMService(config_loader)

# 处理收到的消息
def on_message(ws, message):
    try:
        print(f"Received: {message}")        
    except Exception as e:
        logger.error(f"Error while handling message: {e}")

# 处理 WebSocket 错误
def on_error(ws, error):
    logger.error(f"Error: {error}")

# 处理 WebSocket 关闭
def on_close(ws, close_status_code, close_msg):
    logger.info(f"Connection closed: {close_status_code}, {close_msg}")

# WebSocket 连接成功时的回调
def on_open(ws):
    logger.info("WebSocket connection opened.")
    
    # 发送设备 ID 进行鉴权
    device_id = "device_001"  # 替换为实际的设备 ID
    
    # 发送设备 ID 进行鉴权
    ws.send(device_id)
    logger.info(f"Sent device ID: {device_id}")

    # 发送初始化消息等（如果需要）
    init_message = {"text": "Hello, WebSocket!"}
    ws.send(json.dumps(init_message))  # 向服务器发送初始化消息

# 启动 WebSocket 客户端
def start_websocket():
    ws_url = "ws://lab-cqu.dxh-wds.top:8000/ws"  # 替换为实际的 WebSocket URL

    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    # 使用线程启动 WebSocket 客户端
    thread = threading.Thread(target=start_websocket)
    thread.start()
