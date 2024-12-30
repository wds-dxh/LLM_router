import asyncio
import websockets

async def test_websocket():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri, extra_headers={"device-id": "test_device_id"}) as websocket:
        try:
            # 发送测试消息
            await websocket.send("你好，LLM！")
            print("发送消息: 你好，LLM！")

            # 接收响应
            response = await websocket.recv()
            print(f"收到响应: {response}")

        except websockets.exceptions.ConnectionClosed as e:
            print(f"连接关闭: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())
