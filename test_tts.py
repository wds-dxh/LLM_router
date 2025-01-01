import asyncio
import time
from app.services.tts_service import TTSService


async def test_single_request(tts_service, text: str, index: int):
    start_time = time.time()
    result = await tts_service.synthesize(text)
    end_time = time.time()

    if result["success"]:
        print(f"Request {index} completed in {end_time - start_time:.2f}s")
        # 保存音频文件用于验证
        with open(f"test_output_{index}.mp3", "wb") as f:
            f.write(result["audio_data"])
    else:
        print(f"Request {index} failed: {result.get('error')}")

    return result


async def test_concurrent_requests(num_requests: int = 10):
    async with TTSService() as tts:
        # 准备测试文本
        test_texts = [
            f"这是第{i+1}条测试消息，测试TTS服务的并发性能,测试TTS服务的并发性能,测试TTS服务的并发性能,测试TTS服务的并发性能,测试TTS服务的并发性能," for i in range(num_requests)
        ]

        print(f"开始测试 {num_requests} 个并发请求...")
        start_time = time.time()

        tasks = [
            test_single_request(tts, text, i)
            for i, text in enumerate(test_texts)
        ]

        results = await asyncio.gather(*tasks)
        end_time = time.time()

        # 统计结果
        success_count = sum(1 for r in results if r["success"])
        total_time = end_time - start_time
        avg_time = total_time / num_requests

        print("\n测试结果统计:")
        print(f"总请求数: {num_requests}")
        print(f"成功请求: {success_count}")
        print(f"失败请求: {num_requests - success_count}")
        print(f"总耗时: {total_time:.2f}秒")
        print(f"平均耗时: {avg_time:.2f}秒/请求")
        print(f"QPS: {num_requests/total_time:.2f}请求/秒")

if __name__ == "__main__":
    print("=== 测试并发合成 ===")
    asyncio.run(test_concurrent_requests(1))
