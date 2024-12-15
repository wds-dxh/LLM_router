'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-13 00:52:23
Description: 数据库初始化启动脚本
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
import os
import sys

# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# 导入并运行初始化函数
from app.scripts.init_database import initialize_database

if __name__ == "__main__":
    initialize_database()