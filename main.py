'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-13 00:52:23
Description: 主程序
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
from robyn import Robyn
from app.utils.database import init_db

app = Robyn(__file__)

# 初始化数据库
init_db()

if __name__ == "__main__":
    app.start()
