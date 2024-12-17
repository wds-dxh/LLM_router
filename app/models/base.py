'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-17 05:55:24
Description: 基础模型接口
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseModel(ABC):
    """基础模型接口"""
    
    @abstractmethod
    async def create(self, **kwargs) -> Dict[str, Any]:
        """创建记录"""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """通过ID获取记录"""
        pass
    
    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """获取所有记录"""
        pass
    
    @abstractmethod
    async def update(self, id: int, **kwargs) -> bool:
        """更新记录"""
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> bool:
        """删除记录"""
        pass 