import asyncio
import os
from app.services.tts_service import TTSService
from app.utils.config_loader import ConfigLoader

async def test_single_text(tts_service):
    """测试单段文本合成"""
    print("\n=== 测试单段文本合成 ===")
    text = "你好，这是单段文本测试。"
    
    async def single_text_generator():
        yield (text, True)
        yield ("", False)
    
    async for chunk in tts_service.synthesize_stream(single_text_generator()):
        if chunk["type"] == "audio_chunk":
            print(f"Received audio chunk: {len(chunk['chunk'])} bytes")
            with open("single_text.pcm", "ab") as f:
                f.write(chunk["chunk"])
        elif chunk["type"] == "done":
            print("Single text synthesis completed")

async def test_stream_text(tts_service):
    """测试流式文本合成"""
    print("\n=== 测试流式文本合成 ===")
    
    async def text_generator():
        texts = [
            ("第一段文本，", True),
            ("第二段文本，", True),
            ("第三段文本。", False)
        ]
        for t in texts:
            yield t
            await asyncio.sleep(0.1)  # 模拟文本间隔

    async for chunk in tts_service.synthesize_stream(text_generator()):
        if chunk["type"] == "audio_chunk":
            print(f"Received audio chunk: {len(chunk['chunk'])} bytes")
            with open("stream_text.pcm", "ab") as f:
                f.write(chunk["chunk"])
        elif chunk["type"] == "done":
            print("Stream synthesis completed")

async def main():
    config_loader = ConfigLoader()
    
    async with TTSService(config_loader) as tts_service:
        # 运行测试
        # await test_single_text(tts_service)
        await test_stream_text(tts_service)

if __name__ == "__main__":
    asyncio.run(main())
