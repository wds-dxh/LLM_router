from fastapi import WebSocket, WebSocketDisconnect
from services.auth_service import AuthService
from services.speech_to_text import ASRClient

auth_service = AuthService()
asr_client = ASRClient()

async def websocket_handler(websocket: WebSocket):
    await websocket.accept()
    try:
        # 接收认证信息
        auth_data = await websocket.receive_json()
        device_name = auth_data.get("device_name")
        api_key = auth_data.get("api_key")

        # 验证设备
        if not auth_service.authenticate_device(device_name, api_key):
            await websocket.close(code=1008)  # 关闭连接，认证失败
            return

        # 接收音频数据
        audio_data = await websocket.receive_bytes()
        print(f"Received audio data of length: {len(audio_data)}")
        
        # 进行语音识别 - 确保这是异步调用
        result_text = await asr_client.recognize_audio_stream(audio_data)  # 添加 await
        
        # 发送识别结果
        await websocket.send_text(result_text)

    except WebSocketDisconnect:
        print(f"WebSocket连接断开: {device_name}")
    except Exception as e:
        print(f"处理WebSocket连接时出错: {str(e)}")
        await websocket.close(code=1011)  # 关闭连接，服务器错误
