'''
Author: wds2dxh wdsnpshy@163.com
Date: 2025-01-10 14:39:13
Description: 
Copyright (c) 2025 by ${wds2dxh}, All Rights Reserved. 
'''
import json
import asyncio
import os
import time
import websockets

# 定义一个用于处理接收到消息的回调函数

time_1 = 0
time_2 = 0


async def handle_message(response):
    # print(f"Received: {response}")
    # 不换行输出
    global time_1
    global time_2
    time_2 = time.time()    # 单位是秒
    print(f"Received: {response}, time: {time_2 - time_1}")

    # os._exit(0)


async def test_websocket():
    global time_1
    # uri = "ws://lab-cqu.dxh-wds.top:8000/ws"
    uri = "ws://47.108.223.146:8000/ws"
    device_id = "device_002"  # 替换为实际的 device_id

    for attempt in range(3):  # 尝试重连3次
        try:
            async with websockets.connect(uri) as websocket:
                # 发送 device_id 进行鉴权
                await websocket.send(device_id)

                # 发送对话请求
                chat_message = json.dumps({"text": "你是谁？"})
                time_1 = time.time()
                await websocket.send(chat_message)

                # 注册接收到消息时调用的回调函数
                while True:
                    try:
                        # 等待并接收消息
                        response = await websocket.recv()
                        await handle_message(response)  # 调用回调函数处理接收到的消息

                    except websockets.ConnectionClosed as e:
                        print(f"Connection closed: {e.code}, {e.reason}")
                        break  # 连接关闭，跳出循环
                break  # 成功连接后退出重试循环

        except Exception as e:
            print(f"Error during connection attempt {attempt + 1}: {e}")
            await asyncio.sleep(1)  # 等待1秒后重试


async def main():
    # 启动多个 WebSocket 客户端
    tasks = [asyncio.create_task(test_websocket())
             for _ in range(1)]  # 减少并发连接数
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
