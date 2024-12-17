'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-17 05:18:15
Description: 鉴权中间件，负责验证API Key和获取权限信息。
'''

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.models.api_key import ApiKeyModel
from app.utils.logger import get_logger

logger = get_logger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    """鉴权中间件：基于设备ID和API Key进行验证"""

    async def dispatch(self, request: Request, call_next):
        """
        拦截请求并进行鉴权
        """
        device_id = request.headers.get("device-id")
        if not device_id:
            raise HTTPException(status_code=400, detail="Bad Request: Missing 'device-id' header")

        api_key_model = ApiKeyModel()

        try:
            # 查询 API Key 和权限
            api_key_record = await api_key_model.get_by_device_id(device_id)
            if not api_key_record:  # 如果 API Key 不存在，则拒绝访问
                raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

            # 假设 api_key_record 是一个元组，其中索引 0 是 api_key，索引 1 是 status
            api_key = api_key_record[1]  # 获取 API Key
            status = api_key_record[4]   # 获取状态

            if status != 'active':
                raise HTTPException(status_code=403, detail="Forbidden: Inactive API Key")

            permissions = await api_key_model.get_permissions(api_key)
            if not permissions:
                raise HTTPException(status_code=403, detail="Forbidden: No permissions assigned")

            # 缓存 API Key 和权限到 request.state
            request.state.auth = {
                "api_key": api_key,
                "permissions": {perm[1] for perm in permissions}  # 权限名在最后一个位置
            }
            logger.info(f"Authentication successful for device_id: {device_id}")

        except HTTPException as e:
            logger.error(f"Authentication failed: {e.detail}")
            raise e

        # 继续处理请求
        response = await call_next(request)
        return response
