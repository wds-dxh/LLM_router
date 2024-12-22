import asyncio
import time
from app.utils.config_loader import ConfigLoader
from app.services.stt_service import STTService

async def recognize_stt(stt_service, audio_data):
    # 执行语音识别
    time_now = time.time()
    result = await stt_service.recognize(audio_data)
    print(f"Time cost: {time.time() - time_now:.2f}s")
    return result

async def main():
    config_loader = ConfigLoader()
    async with STTService(config_loader) as stt_service:
        # 读取音频文件
        with open('./output.wav', 'rb') as f:
            audio_data = f.read()

        # 同时启动两个语音识别任务
        tasks = [
            recognize_stt(stt_service, audio_data),
            recognize_stt(stt_service, audio_data),
            recognize_stt(stt_service, audio_data),
            recognize_stt(stt_service, audio_data)
        ]
        
        # 等待两个任务完成
        results = await asyncio.gather(*tasks)

        # 打印两个任务的结果
        for i, result in enumerate(results, 1):
            print(f"Result from task {i}: {result}")

if __name__ == "__main__":
    time_now = time.time()
    asyncio.run(main())
    print("Time cost1111:", time.time() - time_now)