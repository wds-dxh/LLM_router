'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-15 16:10:21
Description: TTS服务测试脚本
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
import os
import sys
import time

# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app.services.text_to_speech import TTSService

def test_tts():
    tts_service = TTSService()
    text = "字节跳动语音合成字节跳动语音合成字节跳动语音合成字节跳动语音合成字节跳动语音合成字节跳动语音合成字节跳动语音合成字节跳动语音合成"
    try:
        time_start = time.time()
        audio_data = tts_service.synthesize(text)
        time_end = time.time()
        
        print("TTS合成耗时：", time_end - time_start)
        with open("output.mp3", "wb") as f:
            f.write(audio_data)
        print("TTS合成成功，音频已保存为output.mp3")
    except Exception as e:
        print(f"TTS合成失败: {str(e)}")

if __name__ == "__main__":
    test_tts()
