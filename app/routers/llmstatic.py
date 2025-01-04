import asyncio
import logging
import os
import uuid
from fastapi import APIRouter, Request, HTTPException, Header
from typing import Optional
from app.utils.config_loader import ConfigLoader
from app.services.llm_service import LLMService
from app.services.tts_service import TTSService

logger = logging.getLogger(__name__)
router = APIRouter()

config_loader = ConfigLoader()
llm_service = LLMService(config_loader)
tts_service = TTSService()

# 音频文件存储目录
AUDIO_DIR = "static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)


async def process_llm_response_and_save(device_id: str, text: str):
    """
    处理LLM响应并保存为音频文件
    """
    try:
        accumulated_text = ""
        audio_data = bytearray()

        async for chunk in llm_service.chat_stream(device_id, text):
            if chunk.get('type') == 'content':
                accumulated_text += chunk['text']

                if any(accumulated_text.endswith(suffix) for suffix in ['。', '！', '!', '.', '？', '?', '；', ';']):
                    index = max(accumulated_text.rfind(suffix) for suffix in [
                        '。', '！', '!', '.', '？', '?', '；', ';'])
                    sentence = accumulated_text[:index + 1]

                    # 生成音频数据
                    audio_chunk = await tts_service.synthesize(sentence)
                    audio_data.extend(audio_chunk['audio_data'])

                    accumulated_text = accumulated_text[index + 1:]

        # 生成唯一文件名
        file_name = f"{uuid.uuid4()}.pcm"
        file_path = os.path.join(AUDIO_DIR, file_name)

        # 保存音频文件
        with open(file_path, 'wb') as f:
            f.write(audio_data)

        # 返回文件下载链接
        download_url = f"/api/v1/audio/{file_name}"
        return {"status": "success", "download_url": download_url}

    except Exception as e:
        logger.error(f"Error in processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/static-chat")
async def static_chat(request: Request, device_id: Optional[str] = Header(None)):
    """
    处理聊天请求并返回音频文件下载链接
    """
    if not device_id:
        raise HTTPException(
            status_code=400, detail="Missing 'device-id' header")

    body = await request.json()
    if 'text' not in body:
        raise HTTPException(status_code=400, detail="Missing 'text' field")

    text = body['text']
    result = await process_llm_response_and_save(device_id, text)
    return result


@router.get("/audio/{file_name}")
async def get_audio(file_name: str):
    """
    提供音频文件下载
    """
    file_path = os.path.join(AUDIO_DIR, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    return {'file_path': file_path}
