import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/test_device_id"
    async with websockets.connect(uri) as websocket:
        try:
            # 发送测试消息
            await websocket.send("你好，LLM！")
            print("发送消息: 你好，LLM！")

            # 接收流式响应
            while True:
                response = await websocket.recv()
                print(f"收到响应: {response}")

        except websockets.exceptions.ConnectionClosed as e:
            print(f"连接关闭: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())
