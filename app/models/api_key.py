'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-17 05:55:24
Description: API Key模型，主要作用是对API Key进行CRUD操作。用于控制API Key的创建、获取、更新和删除。
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
from typing import List, Dict, Any, Optional
from .base import BaseModel
from .db import DatabaseManager

class ApiKeyModel(BaseModel):
    """API Key模型"""
    TABLE_NAME = "api_keys"
    
    async def create(self, **kwargs) -> Dict[str, Any]: 
        """创建API Key记录"""
        query = f"""
            INSERT INTO {self.TABLE_NAME} 
            (api_key, device_id, description, status) 
            VALUES (%s, %s, %s, %s)
        """
        values = (
            kwargs['api_key'],
            kwargs['device_id'],
            kwargs['description'],
            kwargs.get('status', 'active')
        )
        
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, values)
            return {'id': cursor.lastrowid, **kwargs}
    
    async def get_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """通过ID获取API Key记录"""
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE id = %s"
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (id,))
            result = await cursor.fetchone()
            return result if result else None
    
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """获取所有API Key记录"""
        query = f"SELECT * FROM {self.TABLE_NAME} LIMIT %s OFFSET %s"
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (limit, offset))
            return await cursor.fetchall()
    
    async def update(self, id: int, **kwargs) -> bool:
        """更新API Key记录"""
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = %s")
            values.append(value)
        values.append(id)
        
        query = f"""
            UPDATE {self.TABLE_NAME} 
            SET {', '.join(fields)}
            WHERE id = %s
        """
        
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, tuple(values))
            return cursor.rowcount > 0
    
    async def delete(self, id: int) -> bool:
        """删除API Key记录"""
        query = f"DELETE FROM {self.TABLE_NAME} WHERE id = %s"
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (id,))
            return cursor.rowcount > 0
    
    # 额外的特定方法
    async def get_by_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """通过API Key获取记录"""
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE api_key = %s"
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (api_key,))
            result = await cursor.fetchone()
            return result if result else None
    
    async def get_by_device_id(self, device_id: str) -> Optional[Dict[str, Any]]:
        """通过设备ID获取API Key记录
        返回示例====设备权限 (1, 'sk-test-123456', 'device_001', '测试设备1-完整权限', 'active', datetime.datetime(2024, 12, 17, 8, 4, 48), None)
        """
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE device_id = %s AND status = 'active'"
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (device_id,))
            result = await cursor.fetchone()
            return result if result else None
    
    async def get_permissions(self, api_key: str) -> List[Dict[str, Any]]:
        """获取API Key的权限列表"""
        query = """
            SELECT p.* 
            FROM permissions p
            JOIN api_key_permissions ap ON p.id = ap.permission_id
            JOIN api_keys ak ON ak.id = ap.api_key_id
            WHERE ak.api_key = %s AND ak.status = 'active'
        """
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (api_key,))
            return await cursor.fetchall()
    
    async def add_permission(self, api_key_id: int, permission_id: int) -> bool:
        """为API Key添加权限"""
        query = """
            INSERT INTO api_key_permissions (api_key_id, permission_id)
            VALUES (%s, %s)
        """
        try:
            async with DatabaseManager.get_cursor() as cursor:
                await cursor.execute(query, (api_key_id, permission_id))
                return True
        except Exception:
            return False
    
    async def remove_permission(self, api_key_id: int, permission_id: int) -> bool:
        """移除API Key的权限"""
        query = """
            DELETE FROM api_key_permissions 
            WHERE api_key_id = %s AND permission_id = %s
        """
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (api_key_id, permission_id))
            return cursor.rowcount > 0
    
    async def update_last_used(self, api_key: str) -> bool:
        """更新API Key的最后使用时间"""
        query = f"""
            UPDATE {self.TABLE_NAME}
            SET last_used_at = CURRENT_TIMESTAMP
            WHERE api_key = %s
        """
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (api_key,))
            return cursor.rowcount > 0
