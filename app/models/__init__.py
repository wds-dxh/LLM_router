'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-17 05:55:24
Description: 模型工厂
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
from typing import Dict, Type
from .base import BaseModel
from .api_key import ApiKeyModel
from .permissions import PermissionModel
from .conversations import ConversationModel

class ModelFactory:
    _models: Dict[str, Type[BaseModel]] = {
        'api_key': ApiKeyModel,
        'permission': PermissionModel,
        'conversation': ConversationModel,
    }
    
    @classmethod
    def get_model(cls, model_name: str) -> BaseModel:
        """获取模型实例"""
        model_class = cls._models.get(model_name)
        if not model_class:
            raise ValueError(f"Model {model_name} not found")
        return model_class()

# 导出工厂类和所有模型
__all__ = [
    'ModelFactory',
    'ApiKeyModel',
    'PermissionModel',
    'ConversationModel',
    'STTResultModel',
    'TTSResultModel'
]
