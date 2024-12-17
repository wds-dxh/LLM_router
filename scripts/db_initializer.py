'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-17 05:55:24
Description: 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT')
}
print(DB_CONFIG)


# 读取SQL文件内容
def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# 初始化数据库
def initialize_database(sql_file_path):
    try:
        # 连接到数据库
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 读取并执行SQL脚本
            sql_script = read_sql_file(sql_file_path)
            
            # 使用分号分割SQL语句
            sql_commands = sql_script.split(';')
            
            for command in sql_commands:
                # 跳过空命令
                if command.strip():
                    cursor.execute(command)
                    print(f"Executed SQL command successfully")
            
            connection.commit()
            print("数据库初始化成功！")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    # 首先执行表结构初始化
    sql_schema_path = 'scripts/init_db.sql'
    initialize_database(sql_schema_path)
    
    # 然后执行示例数据初始化
    sql_sample_data_path = 'scripts/initialize_sample_data.sql'
    initialize_database(sql_sample_data_path)

    # # 删除所有表
    # sql_sample_data_path = 'scripts/delete_all_tables.sql'
    # initialize_database(sql_sample_data_path)