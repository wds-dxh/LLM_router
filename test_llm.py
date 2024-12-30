import asyncio
import time
from app.utils.config_loader import ConfigLoader
from app.services.llm_service import LLMService

async def test_basic_chat(llm_service):
    """测试基本对话功能"""
    user_id = "test_user"
    
    
    
    llm_service.set_role("知心大姐姐")
    print(f"当前角色: {llm_service.get_current_role()}")
    # 测试角色管理
    print("\n=== 测试角色管理 ===")
    roles = llm_service.list_available_roles()
    print(f"可用角色: {roles}")

    
    # 测试对话
    print("\n=== 测试对话 ===")
    response = await llm_service.chat(user_id, "我有一百元钱")
    print(f"响应: {response['text']}\n")
    # response = await llm_service.chat(user_id, "你会什么？")
    # print(f"响应: {response['text']}\n")

async def test_stream_chat(llm_service):
    """测试流式对话功能"""
    user_id = "test_user"
    
    llm_service.set_role("儿童心理专家")
    print(f"当前角色: {llm_service.get_current_role()}")
    
    llm_service.set_role("知心大姐姐")
    print(f"当前角色: {llm_service.get_current_role()}")
    
    print("\n=== 测试流式对话 ===")
    print("AI: ", end="", flush=True)

    async for chunk in llm_service.chat_stream(user_id, "你还记得我有多钱吗》"):
        if chunk.get('type') == 'content':
            print(chunk['text'], end="", flush=True)
            print("--------------------------------------------")
    print("\n")

async def test_context_management(llm_service):
    """测试上下文管理"""
    user_id = "test_user"
    
    print("\n=== 测试上下文管理 ===")
    # 测试多轮对话
    await llm_service.chat(user_id, "My name is John")
    response = await llm_service.chat(user_id, "What's my name?")
    print(f"上下文测试响应: {response['text']}")
    
    # 获取上下文摘要
    summary = llm_service.get_context_summary(user_id)
    print(f"上下文摘要: {summary}")
    
    # 清除上下文
    llm_service.clear_context(user_id)
    print("上下文已清除")

async def main():
    config_loader = ConfigLoader()
    
    async with LLMService(config_loader) as llm_service:
        try:
            await test_basic_chat(llm_service)
            # await test_stream_chat(llm_service)
            # await test_context_management(llm_service)
            
        except Exception as e:
            print(f"测试过程中出错: {str(e)}")

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    print(f"\n总耗时: {time.time() - start_time:.2f} 秒")
