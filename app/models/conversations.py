'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-17 05:55:24
Description: 对话记录模型，用于管理LLM对话历史记录
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
from typing import List, Dict, Any, Optional
from datetime import datetime
from .base import BaseModel
from .db import DatabaseManager

class ConversationModel(BaseModel):
    """对话记录模型"""
    TABLE_NAME = "conversations"
    
    async def create(self, **kwargs) -> Dict[str, Any]:
        """创建对话记录"""
        query = f"""
            INSERT INTO {self.TABLE_NAME} 
            (device_id, user_id, input_text, response_text, role, timestamp) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            kwargs['device_id'],
            kwargs['user_id'],
            kwargs['input_text'],
            kwargs['response_text'],
            kwargs.get('role', 'assistant'),
            kwargs.get('timestamp', datetime.now())
        )
        
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, values)
            return {'id': cursor.lastrowid, **kwargs}
    
    async def get_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """通过ID获取对话记录"""
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE id = %s"
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (id,))
            result = await cursor.fetchone()
            return result if result else None
    
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """获取所有对话记录"""
        query = f"SELECT * FROM {self.TABLE_NAME} ORDER BY timestamp DESC LIMIT %s OFFSET %s"
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (limit, offset))
            return await cursor.fetchall()
    
    async def update(self, id: int, **kwargs) -> bool:
        """更新对话记录"""
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
        """删除对话记录"""
        query = f"DELETE FROM {self.TABLE_NAME} WHERE id = %s"
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (id,))
            return cursor.rowcount > 0
    
    # 额外的特定方法
    async def get_by_device_id(self, device_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """获取指定设备的对话记录"""
        query = f"""
            SELECT * FROM {self.TABLE_NAME}
            WHERE device_id = %s
            ORDER BY timestamp DESC
            LIMIT %s OFFSET %s
        """
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (device_id, limit, offset))
            return await cursor.fetchall()
    
    async def get_by_user_id(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """获取指定用户的对话记录"""
        query = f"""
            SELECT * FROM {self.TABLE_NAME}
            WHERE user_id = %s
            ORDER BY timestamp DESC
            LIMIT %s OFFSET %s
        """
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (user_id, limit, offset))
            return await cursor.fetchall()
    
    async def get_conversation_history(self, device_id: str, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取特定设备和用户的最近对话历史"""
        query = f"""
            SELECT * FROM {self.TABLE_NAME}
            WHERE device_id = %s AND user_id = %s
            ORDER BY timestamp DESC
            LIMIT %s
        """
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (device_id, user_id, limit))
            return await cursor.fetchall()
    
    async def delete_by_device_id(self, device_id: str) -> bool:
        """删除指定设备的所有对话记录"""
        query = f"DELETE FROM {self.TABLE_NAME} WHERE device_id = %s"
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (device_id,))
            return cursor.rowcount > 0
    
    async def delete_by_user_id(self, user_id: str) -> bool:
        """删除指定用户的所有对话记录"""
        query = f"DELETE FROM {self.TABLE_NAME} WHERE user_id = %s"
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, (user_id,))
            return cursor.rowcount > 0
    
    async def get_conversation_count(self, device_id: str = None, user_id: str = None) -> int:
        """获取对话记录数量"""
        conditions = []
        values = []
        
        if device_id:
            conditions.append("device_id = %s")
            values.append(device_id)
        if user_id:
            conditions.append("user_id = %s")
            values.append(user_id)
            
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        query = f"""
            SELECT COUNT(*) as count 
            FROM {self.TABLE_NAME}
            WHERE {where_clause}
        """
        
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, tuple(values))
            result = await cursor.fetchone()
            return result['count'] if result else 0
    
    async def search_conversations(
        self,
        keyword: str,
        device_id: str = None,
        user_id: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """搜索对话记录"""
        conditions = ["(input_text LIKE %s OR response_text LIKE %s)"]
        values = [f"%{keyword}%", f"%{keyword}%"]
        
        if device_id:
            conditions.append("device_id = %s")
            values.append(device_id)
        if user_id:
            conditions.append("user_id = %s")
            values.append(user_id)
        if start_date:
            conditions.append("timestamp >= %s")
            values.append(start_date)
        if end_date:
            conditions.append("timestamp <= %s")
            values.append(end_date)
            
        where_clause = " AND ".join(conditions)
        
        query = f"""
            SELECT * FROM {self.TABLE_NAME}
            WHERE {where_clause}
            ORDER BY timestamp DESC
            LIMIT %s OFFSET %s
        """
        values.extend([limit, offset])
        
        async with DatabaseManager.get_cursor() as cursor:
            await cursor.execute(query, tuple(values))
            return await cursor.fetchall()
