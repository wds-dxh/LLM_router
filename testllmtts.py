import asyncio
import json
import logging
import os
import websocket
import threading
import base64
import time

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
time_1 = 0
time_2 = 0


def on_message(ws, message):
    # global time_1, time_2
    # time_2 = time.time()
    # print(f"Time: {time_2 - time_1}")
    # os._exit(0)
    try:
        # 尝试将消息解码为音频数据,不需要解码，tts引擎已经解码
        audio_data = message

        # 生成带时间戳的文件名
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        # filename = f"audio_output_{timestamp}.pcm"
        filename = f"audio_output.pcm"

        # 保存音频文件
        with open(filename, "ab") as f:
            f.write(audio_data)
        logger.info(f"已保存音频文件: {filename}")
    except Exception as e:
        # 如果不是音频数据，尝试作为文本处理
        try:
            # 尝试解析为JSON
            data = json.loads(message)
            logger.info(f"收到文本消息: {data}")
        except:
            # 如果既不是音频也不是JSON，则作为普通文本输出
            logger.info(f"收到消息: {message}")
        logger.error(f"处理消息时出错: {e}")


def on_error(ws, error):
    logger.error(f"WebSocket错误: {error}")


def on_close(ws, close_status_code, close_msg):
    logger.info(f"WebSocket连接关闭: {close_status_code}, {close_msg}")


def on_open(ws):
    global time_1
    logger.info("WebSocket连接已建立")

    # 发送设备ID进行鉴权
    device_id = "device_001"
    ws.send(device_id)
    logger.info(f"已发送设备ID: {device_id}")

    # 发送测试消息
    test_messages = [
        {"text": "讲个笑话吧"},
        # 可以添加更多测试消息
    ]

    def send_messages():
        global time_1
        for msg in test_messages:
            time_1 = time.time()
            ws.send(json.dumps(msg))
            logger.info(f"已发送消息: {msg}")
            # 等待5秒后发送下一条消息
            time.sleep(5)

    # 使用新线程发送消息，避免阻塞WebSocket接收
    threading.Thread(target=send_messages).start()


def start_websocket():
    websocket.enableTrace(True)  # 启用详细日志
    ws_url = "ws://lab-cqu.dxh-wds.top:8000/ws"

    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    logger.info("启动WebSocket测试客户端...")
    # 启动WebSocket客户端
    ws_thread = threading.Thread(target=start_websocket)
    ws_thread.start()

    try:
        # 保持主线程运行
        ws_thread.join()
    except KeyboardInterrupt:
        logger.info("接收到退出信号，程序终止")
