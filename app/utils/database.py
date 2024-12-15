from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.device import Base, Device, DeviceStatus
import json
import os
from datetime import datetime

# 加载配置
def load_config(config_file):
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    with open(config_path, 'r') as f:
        return json.load(f)

# 加载配置
db_config = load_config('../config/db_config.json')

# 导出配置项
DATABASE_URL = db_config['database']['url']

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 初始化数据库表
def init_db():
    Base.metadata.create_all(bind=engine)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_device(device_name: str, api_key: str):
    """添加设备到数据库"""
    db = SessionLocal()
    try:
        # 检查设备是否已存在
        existing_device = db.query(Device).filter(Device.device_name == device_name).first()
        if existing_device:
            print(f"设备 {device_name} 已存在。")
            return

        # 创建新设备
        new_device = Device(
            device_name=device_name,
            api_key=api_key,
            status=DeviceStatus.OFFLINE,
            last_seen=datetime.utcnow(),
            created_at=datetime.utcnow()
        )
        db.add(new_device)
        db.commit()
        print(f"设备 {device_name} 添加成功。")
    except Exception as e:
        db.rollback()
        print(f"添加设备时出错: {str(e)}")
    finally:
        db.close() 