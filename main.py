from robyn import Robyn
from app.utils.database import init_db

app = Robyn(__file__)

# 初始化数据库
init_db()

if __name__ == "__main__":
    app.start()
