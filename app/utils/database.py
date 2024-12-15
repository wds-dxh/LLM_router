from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker # pip install sqlalchemy -i https://pypi.tuna.tsinghua.edu.cn/simple
from app.config.settings import DATABASE_URL
from app.models.device import Base

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