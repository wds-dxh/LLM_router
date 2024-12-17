from typing import AsyncGenerator
import asyncmy
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

class DatabaseManager:
    _pool = None

    @classmethod
    async def get_pool(cls):
        """获取数据库连接池"""
        if cls._pool is None:
            cls._pool = await asyncmy.create_pool(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                db=os.getenv('DB_NAME', 'test_db'),
                port=int(os.getenv('DB_PORT', '3306')),
                autocommit=True,
                minsize=1,
                maxsize=10
            )
        return cls._pool

    @classmethod
    @asynccontextmanager
    async def get_cursor(cls) -> AsyncGenerator:
        """获取数据库游标"""
        pool = await cls.get_pool() # 先获取连接池
        async with pool.acquire() as conn:  # 从连接池中获取连接
            async with conn.cursor() as cursor: # 从连接中获取游标
                yield cursor  # 直接返回游标，不提前访问 description

    @classmethod
    async def close_pool(cls):
        """关闭连接池"""
        if cls._pool is not None:
            await cls._pool.close()
            cls._pool = None
