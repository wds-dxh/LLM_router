'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-17 05:18:15
Description: 日志中间件，用于记录请求、响应和异常信息
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved.
'''

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.utils.logger import get_logger

logger = get_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """日志中间件：记录请求和响应信息"""

    async def dispatch(self, request: Request, call_next):
        """
        处理请求并记录日志
        """
        start_time = time.time()

        # 记录请求信息
        client_ip = request.client.host
        method = request.method
        path = request.url.path
        logger.info(f"Incoming request: {method} {path} from {client_ip}")

        try:
            # 继续处理请求
            response: Response = await call_next(request)

            # 记录响应信息
            process_time = time.time() - start_time
            logger.info(
                f"Response: {response.status_code} {method} {path} "
                f"processed in {process_time:.2f}s"
            )

            return response

        except Exception as e:
            # 异常处理
            process_time = time.time() - start_time
            logger.error(
                f"Exception: {str(e)} - {method} {path} "
                f"processed in {process_time:.2f}s"
            )
            raise e
