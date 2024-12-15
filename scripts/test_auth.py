'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-15 22:24:52
Description: 设备认证测试脚本
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
import sys
import os
# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(project_root)
sys.path.append(project_root)

from app.services.auth_service import AuthService

auth_service = AuthService()
print(auth_service.authenticate_device("default_device", "key1"))
