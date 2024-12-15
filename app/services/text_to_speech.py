'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-13 00:52:23
Description: 文本转语音服务
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
import os
import json
import asyncio
from typing import Optional, Dict, Any
import edge_tts  # pip install edge-tts -i https://pypi.tuna.tsinghua.edu.cn/simple
from datetime import datetime

class TTSService:
    def __init__(self):
        """初始化TTS服务"""
        # 加载配置
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'tts_config.json')
        self.config = self._load_config(config_path)
        
        # 创建音频输出目录
        self.output_dir = self.config.get('output_dir', 'data/audio_output')
        os.makedirs(self.output_dir, exist_ok=True)
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 默认配置
                default_config = {
                    "voice": "zh-CN-XiaoxiaoNeural",  # 默认中文女声
                    "rate": "+0%",                     # 语速
                    "volume": "+0%",                   # 音量
                    "output_dir": "data/audio_output"  # 音频输出目录
                }
                # 保存默认配置
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=4, ensure_ascii=False)
                return default_config
        except Exception as e:
            print(f"加载TTS配置失败: {str(e)}")
            return {}

    async def text_to_speech(self, text: str, device_name: str) -> Optional[str]:
        """
        将文本转换为语音
        Args:
            text: 要转换的文本
            device_name: 设备名称（用于生成唯一的文件名）
        Returns:
            str: 生成的音频文件路径，如果失败则返回None
        """
        try:
            # 生成唯一的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{device_name}_{timestamp}.mp3"
            output_path = os.path.join(self.output_dir, filename)
            
            # 创建TTS通信对象
            communicate = edge_tts.Communicate(
                text=text,
                voice=self.config.get('voice', 'zh-CN-XiaoxiaoNeural'),
                rate=self.config.get('rate', '+0%'),
                volume=self.config.get('volume', '+0%')
            )
            
            # 生成音频文件
            await communicate.save(output_path)
            
            print(f"TTS生成成功: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"TTS生成失败: {str(e)}")
            return None
            
    async def get_available_voices(self) -> list:
        """获取所有可用的语音"""
        try:
            voices = await edge_tts.list_voices()
            return voices
        except Exception as e:
            print(f"获取可用语音失败: {str(e)}")
            return []
            
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        更新TTS配置
        Args:
            updates: 要更新的配置项
        Returns:
            bool: 是否更新成功
        """
        try:
            self.config.update(updates)
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'tts_config.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"更新TTS配置失败: {str(e)}")
            return False
