import os
import sys
sys.path.append("/home/wds/workspace/now/LLM_router")  # 添加项目根目录到环境变量

import asyncio
from app.models import (
    ApiKeyModel,
    PermissionModel,
    ConversationModel,
    STTResultModel,
    TTSResultModel
)

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

async def test_permission_model():
    permission_model = PermissionModel()
    
    # 创建权限
    new_permission = await permission_model.create( # 返回的是字典
        permission_name='test_permission',
        description='Test Permission'
    )
    print("创建权限：", new_permission)

    # 根据ID获取权限
    permission = await permission_model.get_by_id(new_permission['id'])
    print("根据ID获取权限：", permission)
    
    # 更新权限描述
    update_result = await permission_model.update(new_permission['id'], description='Updated Description')
    print("更新权限描述：", update_result)
    
    # 获取所有权限
    permissions = await permission_model.get_all()
    print("所有权限：", permissions)

    # 删除权限
    delete_result = await permission_model.delete(new_permission['id'])
    print("删除权限：", delete_result)

async def test_conversation_model():
    conversation_model = ConversationModel()
    
    # 创建对话记录
    new_conversation = await conversation_model.create(
        device_id='test_device_id',
        user_id='test_user_id',
        input_text='Hello',
        response_text='Hi there!'
    )
    print("创建对话记录：", new_conversation)

    # 根据ID获取对话记录
    conversation = await conversation_model.get_by_id(new_conversation['id'])
    print("根据ID获取对话记录：", conversation)
    
    # 更新对话记录
    update_result = await conversation_model.update(new_conversation['id'], response_text='Hello!')
    print("更新对话记录：", update_result)
    
    # 获取所有对话记录
    conversations = await conversation_model.get_all()
    print("所有对话记录：", conversations)

    # 删除对话记录
    delete_result = await conversation_model.delete(new_conversation['id'])
    print("删除对话记录：", delete_result)

async def test_stt_result_model():
    stt_result_model = STTResultModel()
    
    # 创建语音识别记录
    new_stt_result = await stt_result_model.create(
        device_id='test_device_id',
        audio_file_path='/path/to/audio',
        recognized_text='Hello'
    )
    print("创建语音识别记录：", new_stt_result)

    # 根据ID获取语音识别记录
    stt_result = await stt_result_model.get_by_id(new_stt_result['id'])
    print("根据ID获取语音识别记录：", stt_result)
    
    # 更新语音识别记录
    update_result = await stt_result_model.update(new_stt_result['id'], recognized_text='Hi there!')
    print("更新语音识别记录：", update_result)
    
    # 获取所有语音识别记录
    stt_results = await stt_result_model.get_all()
    print("所有语音识别记录：", stt_results)

    # 删除语音识别记录
    delete_result = await stt_result_model.delete(new_stt_result['id'])
    print("删除语音识别记录：", delete_result)

async def test_tts_result_model():
    tts_result_model = TTSResultModel()
    
    # 创建语音合成记录
    new_tts_result = await tts_result_model.create(
        device_id='test_device_id',
        input_text='Hello',
        audio_file_path='/path/to/audio'
    )
    print("创建语音合成记录：", new_tts_result)

    # 根据ID获取语音合成记录
    tts_result = await tts_result_model.get_by_id(new_tts_result['id'])
    print("根据ID获取语音合成记录：", tts_result)
    
    # 更新语音合成记录
    update_result = await tts_result_model.update(new_tts_result['id'], input_text='Hi there!')
    print("更新语音合成记录：", update_result)
    
    # 获取所有语音合成记录
    tts_results = await tts_result_model.get_all()
    print("所有语音合成记录：", tts_results)

    # 删除语音合成记录
    delete_result = await tts_result_model.delete(new_tts_result['id'])
    print("删除语音合成记录：", delete_result)

async def main():
    # await test_api_key_model()
    # await test_permission_model()
    # await test_conversation_model()
    # await test_stt_result_model()
    await test_tts_result_model()

# 运行测试
if __name__ == '__main__':
    asyncio.run(main())