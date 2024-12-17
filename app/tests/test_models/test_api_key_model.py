import os 
import sys
sys.path.append("/home/wds/workspace/now/LLM_router")    # 添加项目根目录到环境变量

import asyncio
from app.models import ApiKeyModel


async def test_api_key_model():
    api_key_model = ApiKeyModel()
    
    # 创建API密钥
    new_api_key = await api_key_model.create(
        api_key='test_api_key',
        device_id='test_device_id',
        description='Test API Key'
    )
    print("创建API密钥：", new_api_key)

    # 根据ID获取API密钥
    api_key = await api_key_model.get_by_id(new_api_key['id'])
    print("根据ID获取API密钥：", api_key)
    
    # 更新API密钥描述
    update_result = await api_key_model.update(new_api_key['id'], description='Updated Description')
    print("更新API密钥描述：", update_result)
    
    # 获取所有API密钥
    api_keys = await api_key_model.get_all()
    print("所有API密钥：", api_keys)

    # 删除API密钥
    delete_result = await api_key_model.delete(new_api_key['id'])
    print("删除API密钥：", delete_result)

    delete_result = await api_key_model.get_by_device_id("device_001")
    print("设备权限",delete_result)


    
    


# 运行测试
if __name__ == '__main__':
    asyncio.run(test_api_key_model())
