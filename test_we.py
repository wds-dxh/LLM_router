import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws"
    device_id = "device_001"  # 替换为实际的 device_id

    async with websockets.connect(uri) as websocket:
        # 发送 device_id 进行鉴权
        await websocket.send(device_id)
        
        try:
            # 发送对话请求
            chat_message = json.dumps({"text": "你是谁"})
            await websocket.send(chat_message)
            response = await websocket.recv()
            print(f"Received: {response}")
            
        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e.code}, {e.reason}")
        finally:
            await websocket.close()

if __name__ == "__main__":
    asyncio.run(test_websocket())
