'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-13 02:16:23
Description: STT服务测试脚本
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
import os
import sys
import asyncio
# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app.services.speech_to_text import ASRClient

async def main():
    # 识别PCM数据流(例如已读取到的PCM二进制数据)
    with open("./output.pcm", "rb") as f:
        pcm_data = f.read()
    client = ASRClient()
    result_text_stream = await client.recognize_audio_stream(pcm_data)
    print("流识别结果:", result_text_stream)

# 使用示例
if __name__ == "__main__":
    asyncio.run(main())


