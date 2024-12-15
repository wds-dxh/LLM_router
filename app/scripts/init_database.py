'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-13 00:52:23
Description: 数据库初始化脚本
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
import mysql.connector
from app.config.settings import DATABASE_URL
from app.utils.database import init_db

def create_database():
    # 解析DATABASE_URL
    db_params = DATABASE_URL.replace('mysql+pymysql://', '').split('/')
    db_name = db_params[-1]
    connection_params = db_params[0].split('@')
    user_pass = connection_params[0].split(':')
    host_port = connection_params[1].split(':')

    config = {
        'user': user_pass[0],
        'password': user_pass[1],
        'host': host_port[0],
        'port': host_port[1]
    }

    try:
        # 连接MySQL服务器
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 检查数据库是否存在
        cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
        exists = cursor.fetchone()

        if not exists:
            # 创建数据库
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"数据库 {db_name} 创建成功")
        else:
            print(f"数据库 {db_name} 已存在")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"创建数据库时出错: {str(e)}")
        return False

    return True

def initialize_database():
    """初始化数据库和表"""
    try:
        # 1. 创建数据库
        if create_database():
            # 2. 创建表
            init_db()
            print("数据库表创建成功")
            return True
    except Exception as e:
        print(f"初始化数据库时出错: {str(e)}")
        return False

if __name__ == "__main__":
    initialize_database() 