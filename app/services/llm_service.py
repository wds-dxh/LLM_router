'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-13 00:52:23
Description: LLM服务
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
import os
from typing import Dict, Any, Optional
from utils.llm import OpenAIAssistant

class LLMService:
    def __init__(self):
        """初始化LLM服务"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'llm_config.json') # 获取LLM配置文件路径
        self.assistant = OpenAIAssistant(config_path)
        
    async def process_text(self, device_name: str, text: str, role_type: Optional[str] = None) -> Dict[str, Any]:
        """
        处理文本请求
        Args:
            device_name: 设备名称（用作用户ID）
            text: 用户输入的文本
            role_type: 可选的角色类型
        Returns:
            Dict: 包含响应文本的字典
        """
        try:
            # 使用设备名称作为用户ID
            response = self.assistant.chat(device_name, text, role_type)
            
            if "error" in response:
                return {
                    "success": False,
                    "error": response["error"],
                    "device_name": device_name
                }
                
            return {
                "success": True,
                "response": response["response"],
                "device_name": device_name,
                "role": response["current_role"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "device_name": device_name
            }
    
    async def process_text_stream(self, device_name: str, text: str, role_type: Optional[str] = None):
        """
        流式处理文本请求
        Args:
            device_name: 设备名称（用作用户ID）
            text: 用户输入的文本
            role_type: 可选的角色类型
        Yields:
            Dict: 包含响应片段的字典
        """
        try:
            async for chunk in self.assistant.chat_stream(device_name, text, role_type):
                if "error" in chunk:
                    yield {
                        "success": False,
                        "error": chunk["error"],
                        "device_name": device_name
                    }
                    return
                    
                yield {
                    "success": True,
                    "content": chunk.get("content", ""),
                    "type": chunk["type"],
                    "device_name": device_name,
                    "role": chunk["current_role"]
                }
                
        except Exception as e:
            yield {
                "success": False,
                "error": str(e),
                "device_name": device_name
            }
    
    def clear_context(self, device_name: str) -> None:
        """清除设备的对话上下文"""
        self.assistant.clear_context(device_name)
