'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-13 00:52:23
Description: LLM服务测试脚本
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
import os
import sys
import asyncio

# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app.services.llm_service import LLMService

async def test_llm():
    # 初始化LLM服务
    llm_service = LLMService()
    
    # 测试设备名称
    device_name = "test_device_001"
    
    # 测试普通对话
    print("\n=== 测试普通对话 ===")
    response = await llm_service.process_text(
        device_name=device_name,
        text="你好，请介绍一下你自己",
        role_type="default"
    )
    print("设备名称:", response.get("device_name"))
    print("角色:", response.get("role"))
    print("响应:", response.get("response"))
    print("成功:", response.get("success"))
    
    # 测试流式对话
    print("\n=== 测试流式对话 ===")
    print("设备名称:", device_name)
    print("响应: ", end="", flush=True)
    
    # 使用同步方式处理流式响应
    async for chunk in llm_service.process_text_stream(
        device_name=device_name,
        text="讲个笑话",
        role_type="default"
    ):
        if chunk.get("success"):
            if chunk.get("type") == "content":
                print(chunk.get("content"), end="", flush=True)
            elif chunk.get("type") == "done":
                print()  # 换行
        else:
            print(f"\n错误: {chunk.get('error')}")
    
    # 测试上下文
    print("\n=== 测试上下文对话 ===")
    response1 = await llm_service.process_text(
        device_name=device_name,
        text="我的名字叫小明",
    )
    print("第一轮响应:", response1.get("response"))
    
    response2 = await llm_service.process_text(
        device_name=device_name,
        text="我刚才说我叫什么名字？",
    )
    print("第二轮响应:", response2.get("response"))
    
    # 清理上下文
    llm_service.clear_context(device_name)
    print("\n测试完成！")

if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_llm()) 