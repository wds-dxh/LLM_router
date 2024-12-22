
import logging
from logging.handlers import TimedRotatingFileHandler
import os

def get_logger(name: str):
    """
    获取日志记录器
    """
    # 日志目录
    log_dir = "./logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 日志文件路径
    log_file = os.path.join(log_dir, "app.log")

    # 配置日志格式
    logger = logging.getLogger(name)    # 创建日志记录器
    logger.setLevel(logging.INFO)# 设置日志级别

    # 防止重复添加处理器
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # 文件输出（每日生成一个新文件）
        file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8")
        file_handler.setFormatter(formatter)

        # 添加处理器
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
