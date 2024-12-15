import asyncio
import websockets
import json

async def send_audio_data():
    uri = "ws://127.0.0.1:8000/ws"
    async with websockets.connect(uri) as websocket:
        # 发送设备名称和API密钥进行认证
        auth_data = {
            "device_name": "example_device",
            "api_key": "key1"
        }
        await websocket.send(json.dumps(auth_data))

        # 发送音频数据
        with open("output.pcm", "rb") as audio_file:
            audio_data = audio_file.read()
            await websocket.send(audio_data)   

        # 接收识别结果
        result = await websocket.recv()
        print(f"识别结果: {result}")

asyncio.run(send_audio_data())