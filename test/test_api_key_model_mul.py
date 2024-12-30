import os
import sys
sys.path.append("/home/wds/workspace/now/LLM_router")    # 添加项目根目录到环境变量
import asyncio
import time
import uuid  # 用于生成唯一值
from app.models import ApiKeyModel


async def test_api_key_model(task_id):
    """单个 API 密钥的测试操作"""
    api_key_model = ApiKeyModel()
    
    # 为每个任务生成唯一的 API Key
    unique_api_key = f"test_api_key_{task_id}_{uuid.uuid4().hex[:6]}"
    unique_device_id = f"test_device_id_{task_id}"
    
    # 创建API密钥
    new_api_key = await api_key_model.create(
        api_key=unique_api_key,
        device_id=unique_device_id,
        description=f"Test API Key {task_id}"
    )
    
    # 根据ID获取API密钥
    await api_key_model.get_by_id(new_api_key['id'])
    
    # 更新API密钥描述
    await api_key_model.update(new_api_key['id'], description=f"Updated Description {task_id}")
    
    # 获取所有API密钥
    await api_key_model.get_all()
    
    # 删除API密钥
    await api_key_model.delete(new_api_key['id'])


async def run_load_test(concurrent_tasks=100):
    """压测脚本，执行指定数量的并发任务"""
    start_time = time.perf_counter()

    # 创建多个任务，并为每个任务分配唯一的 task_id
    tasks = [test_api_key_model(task_id) for task_id in range(concurrent_tasks)]

    # 并发执行任务
    await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    print(f"压测完成：{concurrent_tasks} 个任务同时执行")
    print(f"总耗时：{end_time - start_time:.2f} 秒")
    print(f"平均每个任务耗时：{(end_time - start_time) / concurrent_tasks:.6f} 秒")


# 运行压测
if __name__ == '__main__':
    concurrent_tasks = 1000  # 定义并发任务数量
    asyncio.run(run_load_test(concurrent_tasks))
