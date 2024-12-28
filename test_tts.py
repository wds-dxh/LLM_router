import asyncio
from app.services.tts_service import TTSService
from app.utils.config_loader import ConfigLoader

async def main():
    config_loader = ConfigLoader(config_directory="config")
    tts_service = TTSService(config_loader)

    async with tts_service:
        # 设置回调函数（可选）
        def on_tts_result(result):
            print("TTS callback:", result)

        tts_service.set_callback(on_tts_result)

        # 一次性合成示例
        text = "你好，这是一段文本合成演示。"
        result = await tts_service.synthesize(text)
        print("Synthesize result:", result)

        # 流式合成示例
        async def text_chunks():
            # 模拟分段文本
            texts = ["当我们", "遇见人工", "智能"]
            for t in texts:
                yield t
                await asyncio.sleep(0.1)

        async for chunk in tts_service.synthesize_stream(text_chunks()):
            print("Stream chunk:", chunk)

if __name__ == "__main__":
    asyncio.run(main())
