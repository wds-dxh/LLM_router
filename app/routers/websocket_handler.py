from fastapi import WebSocket, WebSocketDisconnect
from services.auth_service import AuthService
from services.speech_to_text import ASRClient
from services.llm_service import LLMService
from services.text_to_speech import TTSService
from services.text_to_speech import TTSSynthesisError
import requests
import json
import base64

auth_service = AuthService()
asr_client = ASRClient()
llm_service = LLMService()
tts_service = TTSService()

async def websocket_handler(websocket: WebSocket):
    try:
        await websocket.accept()
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
 
        
        # 进行语音识别 - 确保这是异步调用
        result_text = await asr_client.recognize_audio_stream(audio_data)  # 添加 await

        print("识别结果: ", result_text)
        # 连接大模型进行对话处理
        result_text = await llm_service.process_text(
            device_name=device_name,
            text=result_text,
            role_type="default"
        )
        
        result_text = result_text["response"]
        # 语音合成最长1024个字符
        if len(result_text) > 100:
            result_text = result_text[:100]

        print("识别结果: ", result_text)
        # 使用tts服务
        audio_data = await tts_service.synthesize(result_text, device_name)

        # 发送合成的音频数据
        await websocket.send_bytes(audio_data)
        print("音频数据发送完成")

    except WebSocketDisconnect:
        print(f"WebSocket连接断开: {device_name}")
    except Exception as e:
        print(f"WebSocket处理总体错误: {type(e).__name__}: {str(e)}")
        await websocket.close(code=1011)

