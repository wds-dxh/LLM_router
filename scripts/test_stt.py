'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-13 02:16:23
Description: STT服务测试脚本
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
import os
import sys
# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app.services.speech_to_text import ASRClient


# 使用示例
if __name__ == "__main__":


    # # 识别文件
    # result_text = client.recognize_audio_file("../audio/asr_example.pcm")
    # print("识别结果:", result_text)

    # 识别PCM数据流(例如已读取到的PCM二进制数据)
    with open("./data/audio_output/asr_example.pcm", "rb") as f:
        pcm_data = f.read()
    client = ASRClient()
    result_text_stream = client.recognize_audio_stream(pcm_data)
    print("流识别结果:", result_text_stream)
    # 启动多个线程同时识别文件


    
    # import threading
    # import time
    # def run():
    #     client = ASRClient()
    #     result_text = client.recognize_audio_file("./data/audio_output/asr_example.pcm")
    #     print("识别结果:", result_text)

    # threads = []
    # time_start = time.time()
    # for i in range(100):
    #     t = threading.Thread(target=run)
    #     threads.append(t)
    #     t.start()
    # for t in threads:
    #     t.join()    # 等待线程结束
    # time_end = time.time()
    # print("多线程耗时：", (time_end - time_start)/100)
    # print("识别结束")


