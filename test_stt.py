import asyncio
import time
from app.utils.config_loader import ConfigLoader
from app.services.llm_service import LLMService

async def test_chat(llm_service, user_id: str, message: str):
    """测试基本对话"""
    print(f"\nTesting chat with message: {message}")
    result = await llm_service.chat(user_id, message)
    print(f"Response: {result['text']}")
    return result

async def test_stream_chat(llm_service, user_id: str, message: str):
    """测试流式对话"""
    print(f"\nTesting stream chat with message: {message}")
    async for chunk in llm_service.chat_stream(user_id, message):
        if chunk.get('type') == 'content':
            print(chunk['text'], end='', flush=True)
    print()

async def main():
    config_loader = ConfigLoader()
    
    async with LLMService(config_loader) as llm_service:
        user_id = "test_user"
        
        # 测试角色管理
        print("\nAvailable roles:", llm_service.list_available_roles())
        llm_service.set_role("professional")
        print("Current role:", llm_service.get_current_role())
        
        # 测试基本对话
        await test_chat(llm_service, user_id, "What is Python?")
        
        # 测试流式对话
        await test_stream_chat(llm_service, user_id, "Tell me a short story")
        
        # 测试获取历史记录
        history = await llm_service.get_conversation_history(user_id)
        print("\nConversation history:")
        for conv in history:
            print(f"Time: {conv['timestamp']}")
            for msg in conv['messages']:
                print(f"{msg['role']}: {msg['content']}")
            print("-" * 50)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    print(f"\nTotal time: {time.time() - start_time:.2f} seconds")