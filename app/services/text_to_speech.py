'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-15 16:10:21
Description: TTS服务
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
import os
import json
import uuid
import base64
import requests
from typing import Dict, Any

class TTSSynthesisError(Exception):
    """自定义异常类，用于处理TTS合成错误"""
    pass

class TTSService:
    def __init__(self, config_path=None):
        """初始化TTS服务"""
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '../config/tts_config.json')
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.api_url = f"https://{self.config['host']}/api/v1/tts"
        self.headers = {"Authorization": f"Bearer;{self.config['token']}"}

    def synthesize(self, text: str, user_id: str = "default_user") -> bytes:
        """
        合成文本为语音
        Args:
            text: 要合成的文本
            user_id: 用户ID，用于标识请求
        Returns:
            bytes: 合成���音频数据
        """
        request_json = {
            "app": {
                "appid": self.config['appid'],
                "token": self.config['token'],
                "cluster": self.config['cluster']
            },
            "user": {
                "uid": user_id
            },
            "audio": {
                "voice_type": self.config['voice_type'],
                "encoding": self.config['encoding'],
                "speed_ratio": self.config['speed_ratio'],
                "volume_ratio": self.config['volume_ratio'],
                "pitch_ratio": self.config['pitch_ratio'],
                "emotion": self.config.get('emotion', ''),
                "language": self.config.get('language', 'cn')
            },
            "request": {
                "reqid": str(uuid.uuid4()),
                "text": text,
                "text_type": "plain",
                "operation": "query",
                "with_frontend": 1,
                "frontend_type": "unitTson"
            }
        }

        try:
            response = requests.post(self.api_url, json=request_json, headers=self.headers)
            response_data = response.json()
            if "data" in response_data:
                return base64.b64decode(response_data["data"])  # 返回解码后的音频数据
            else:
                raise TTSSynthesisError(f"TTS合成失败: {response_data.get('error', '未知错误')}")
        except Exception as e:
            raise TTSSynthesisError(f"TTS合成请求失败: {str(e)}")

    def update_settings(self, new_settings: Dict[str, Any]) -> None:
        """
        更新TTS服务的设置
        Args:
            new_settings: 包含新设置的字典
        """
        self.config.update(new_settings)
