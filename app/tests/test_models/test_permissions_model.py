import os 
import sys
sys.path.append("/home/wds/workspace/now/LLM_router")    # 添加项目根目录到环境变量

import asyncio
from app.models import ApiKeyModel


async def test_api_key_model():
    api_key_model = ApiKeyModel()
    
    aa = await api_key_model.get_permissions('sk-test-345678')
    print(aa)


# 运行测试
if __name__ == '__main__':
    asyncio.run(test_api_key_model())
