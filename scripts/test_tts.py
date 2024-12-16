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
import asyncio
# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app.services.text_to_speech import TTSService

async def test_tts():
    """异步测试函数"""
    tts_service = TTSService()
    text = "我觉得作业好难啊！我觉得作业好难啊！我觉得作业好难啊！我觉得作业好难啊！我觉得作业好难啊！我觉得作业好难啊！我觉得作业好难啊！我觉得作业好难啊！我觉得作业好难啊！"
    try:
        print("开始TTS合成测试...")
        time_start = time.time()
        
        # 异步调用合成方法
        audio_data = await tts_service.synthesize(text)
        
        time_end = time.time()
        print(f"TTS合成耗时：{time_end - time_start:.2f}秒")

        # 保存音频文件
        output_file = "output.pcm"
        with open(output_file, "wb") as f:
            f.write(audio_data)
        print(f"TTS合成成功，音频已保存为 {output_file}")
        
    except Exception as e:
        print(f"TTS合成失败: {str(e)}")

def main():
    """主函数"""
    try:
        # 使用 asyncio.run() 运行异步函数
        asyncio.run(test_tts())
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序执行出错: {str(e)}")

if __name__ == "__main__":
    main()
