'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-17 05:55:24
Description: 权限模型，用于管理权限的CRUD操作
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
from typing import List, Dict, Any, Optional
from .base import BaseModel
from .db import DatabaseManager

class PermissionModel(BaseModel):
    """权限模型"""
    TABLE_NAME = "permissions"
    
    async def create(self, **kwargs) -> Dict[str, Any]:
        """创建权限记录"""
        query = f"""
            INSERT INTO {self.TABLE_NAME} 
            (permission_name, description) 
            VALUES (%s, %s)
        """
        values = (kwargs['permission_name'], kwargs.get('description', ''))
        
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, values)
            return {'id': cursor.lastrowid, **kwargs}
    
    async def get_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """通过ID获取权限记录"""
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE id = %s"
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (id,))
            result = await cursor.fetchone()
            return result if result else None
    
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """获取所有权限记录"""
        query = f"SELECT * FROM {self.TABLE_NAME} LIMIT %s OFFSET %s"
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (limit, offset))
            return await cursor.fetchall()
    
    async def update(self, id: int, **kwargs) -> bool:
        """更新权限记录"""
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
        """删除权限记录"""
        query = f"DELETE FROM {self.TABLE_NAME} WHERE id = %s"
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (id,))
            return cursor.rowcount > 0
    
    # 额外的特定方法
    async def get_by_name(self, permission_name: str) -> Optional[Dict[str, Any]]:
        """通过权限名称获取权限记录"""
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE permission_name = %s"
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (permission_name,))
            result = await cursor.fetchone()
            return result if result else None
    
    async def get_api_keys_with_permission(self, permission_name: str) -> List[Dict[str, Any]]:
        """获取拥有指定权限的所有API Key"""
        query = """
            SELECT ak.* 
            FROM api_keys ak
            JOIN api_key_permissions ap ON ak.id = ap.api_key_id
            JOIN permissions p ON p.id = ap.permission_id
            WHERE p.permission_name = %s AND ak.status = 'active'
        """
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (permission_name,))
            return await cursor.fetchall()
    
    async def check_permission(self, api_key: str, permission_name: str) -> bool:
        """检查API Key是否拥有指定权限"""
        query = """
            SELECT COUNT(*) as count
            FROM api_keys ak
            JOIN api_key_permissions ap ON ak.id = ap.api_key_id
            JOIN permissions p ON p.id = ap.permission_id
            WHERE ak.api_key = %s 
            AND p.permission_name = %s 
            AND ak.status = 'active'
        """
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (api_key, permission_name))
            result = await cursor.fetchone()
            return result['count'] > 0 if result else False
