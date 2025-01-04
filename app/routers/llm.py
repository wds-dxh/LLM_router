import asyncio
import logging
from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import StreamingResponse
from typing import Optional
from app.utils.config_loader import ConfigLoader
from app.services.llm_service import LLMService
from app.services.tts_service import TTSService

logger = logging.getLogger(__name__)

router = APIRouter()

config_loader = ConfigLoader()
llm_service = LLMService(config_loader)
tts_service = TTSService()

# 音频缓冲区
shared_audio_buffer = bytearray()
is_streaming_done = False  # 流式传输结束标志

# 定义缓冲区大小
BUFFER_SIZE = 1024 * 2


async def process_llm_response(device_id: str, text: str):
    """
    异步处理 LLM 响应，生成音频并填充到共享缓冲区
    """
    global shared_audio_buffer, is_streaming_done
    accumulated_text = ""

    try:
        async for chunk in llm_service.chat_stream(device_id, text):
            if chunk.get('type') == 'content':
                accumulated_text += chunk['text']

                # 判断是否有完整句子
                if any(accumulated_text.endswith(suffix) for suffix in ['。', '！', '!', '.', '？', '?', '；', ';']):
                    index = max(accumulated_text.rfind(suffix) for suffix in [
                                '。', '！', '!', '.', '？', '?', '；', ';'])
                    sentence = accumulated_text[:index + 1]
                    logger.info(f"Generated sentence: {sentence}")

                    # 生成音频数据
                    audio_data = await tts_service.synthesize(sentence)
                    shared_audio_buffer.extend(audio_data['audio_data'])

                    # 清理已处理部分
                    accumulated_text = accumulated_text[index + 1:]

    except Exception as e:
        logger.error(f"Error in LLM response processing: {str(e)}")
    finally:
        # 标记流结束
        is_streaming_done = True


async def generate_audio_chunks():
    """
    异步生成音频流
    """
    global shared_audio_buffer, is_streaming_done
    try:
        while not is_streaming_done or len(shared_audio_buffer) > 0:
            if len(shared_audio_buffer) >= BUFFER_SIZE:
                chunk = shared_audio_buffer[:BUFFER_SIZE]
                shared_audio_buffer = shared_audio_buffer[BUFFER_SIZE:]
                yield bytes(chunk)  # 确保返回类型为 bytes
            else:
                await asyncio.sleep(0.01)
    except Exception as e:
        logger.error(f"Error in audio chunk generator: {str(e)}")


@router.post("/http-chat")
async def http_chat(request: Request, device_id: Optional[str] = Header(None)):
    """
    HTTP 路由：接收请求并返回流式音频
    """
    global shared_audio_buffer, is_streaming_done
    shared_audio_buffer.clear()
    is_streaming_done = False

    # 解析请求体
    body = await request.json()
    if 'text' not in body:
        raise HTTPException(status_code=400, detail="Missing 'text' field")

    if not device_id:
        raise HTTPException(
            status_code=400, detail="Missing 'device-id' header")

    text = body['text']

    # 启动后台任务处理 LLM 响应
    asyncio.create_task(process_llm_response(device_id, text))

    # 返回流式响应
    headers = {'Content-Type': 'audio/pcm', 'Accept-Ranges': 'bytes'}
    return StreamingResponse(generate_audio_chunks(), headers=headers, media_type='audio/pcm')
