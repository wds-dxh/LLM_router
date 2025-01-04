import requests
import time
import logging
import os

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_chat_request(text: str, save_path: str = "audio_output_http.pcm"):
    """
    发送HTTP请求并保存流式音频数据
    """
    url = "http://lab-cqu.dxh-wds.top:8000/api/v1/http-chat"  # 确保URL与服务端路由一致
    headers = {
        "Content-Type": "application/json",
        "device-id": "device_001"  # 添加设备ID用于鉴权
    }
    data = {"text": text}

    # 清空或创建新文件
    open(save_path, 'wb').close()

    try:
        # 发送请求并启用流式接收
        response = requests.post(url, headers=headers, json=data, stream=True)

        if response.status_code not in [200, 206]:  # 确保返回状态正确
            logger.error(f"请求失败: {response.status_code}")
            return False

        # 获取响应的总长度（如果可用）
        total_size = response.headers.get('Content-Length')
        total_size = int(total_size) if total_size else None

        downloaded_size = 0

        # 分块写入文件
        with open(save_path, 'ab') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # 如果有数据块
                    f.write(chunk)
                    downloaded_size += len(chunk)

                    # 显示进度（如果总长度未知，则只显示已下载大小）
                    if total_size:
                        progress = (downloaded_size / total_size) * 100
                        logger.info(f"下载进度: {progress:.2f}%")
                    else:
                        logger.info(f"已下载: {downloaded_size} 字节")

        logger.info(f"音频文件已保存到: {save_path}")
        return True

    except requests.RequestException as e:
        logger.error(f"请求出错: {str(e)}")
        return False


def main():
    # 测试消息列表
    test_messages = [
        "讲个笑话吧",
        # 可以添加更多测试消息
    ]

    for msg in test_messages:
        logger.info(f"发送消息: {msg}")
        filename = f"audio_output_http.pcm"

        start_time = time.time()
        success = send_chat_request(msg, filename)
        end_time = time.time()

        if success:
            logger.info(f"请求完成，耗时: {end_time - start_time:.2f}秒")
        else:
            logger.error("请求失败")

        # 等待一段时间再发送下一条消息
        time.sleep(2)


if __name__ == "__main__":
    logger.info("启动HTTP测试客户端...")
    try:
        main()
    except KeyboardInterrupt:
        logger.info("接收到退出信号，程序终止")
    except Exception as e:
        logger.error(f"运行出错: {str(e)}")
