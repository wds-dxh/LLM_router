import asyncio
import aiohttp
import json
import os
from datetime import datetime


async def test_static_chat():
    # 测试配置
    base_url = "http://localhost:8000"
    headers = {
        "device-id": "test-device-001",
        "Content-Type": "application/json"
    }
    text = "你是谁？"

    try:
        async with aiohttp.ClientSession() as session:
            # 1. 发送静态聊天请求
            print(f"发送文本: {text}")
            async with session.post(
                f"{base_url}/api/v1/static-chat",
                headers=headers,
                json={"text": text}
            ) as response:
                if response.status != 200:
                    print(f"请求失败: {response.status}")
                    return

                result = await response.json()
                download_url = result.get("download_url")
                if not download_url:
                    print("未获取到下载链接")
                    return

                print(f"获取到下载链接: {download_url}")

                # 2. 下载音频文件
                async with session.get(f"{base_url}{download_url}") as audio_response:
                    if audio_response.status != 200:
                        print(f"下载音频失败: {audio_response.status}")
                        return

                    file_info = await audio_response.json()
                    file_path = file_info.get('file_path')

                    if not file_path or not os.path.exists(file_path):
                        print(f"音频文件不存在: {file_path}")
                        return

                    # 3. 保存音频文件到本地
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    save_path = f"output_{timestamp}.pcm"

                    with open(file_path, 'rb') as src_file:
                        with open(save_path, 'wb') as dst_file:
                            dst_file.write(src_file.read())

                    print(f"音频文件已保存至: {save_path}")
                    print(f"文件大小: {os.path.getsize(save_path)} bytes")

    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")

if __name__ == "__main__":
    print("开始测试静态文件服务...")
    asyncio.run(test_static_chat())
    print("测试完成")
