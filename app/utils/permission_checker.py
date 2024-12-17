from fastapi import Request, HTTPException
from functools import wraps
from typing import Callable
from app.utils.logger import get_logger

logger = get_logger(__name__)

def check_permission(required_permission: str):
    """
    检查当前请求是否具备指定权限
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, request: Request, **kwargs):
            auth = getattr(request.state, "auth", None)     # 从 request.state 中获取鉴权信息
            if not auth:    # 如果没有鉴权信息，则拒绝访问
                raise HTTPException(status_code=401, detail="Unauthorized: Missing authentication context")

            permissions = auth.get("permissions", set())
            if required_permission not in permissions:  # 如果没有指定权限，则拒绝访问
                logger.error(f"Permission denied: '{required_permission}' required but not granted")
                raise HTTPException(status_code=403, detail=f"Forbidden: Missing '{required_permission}' permission")

            logger.info(f"Permission '{required_permission}' granted")
            return await func(*args, request=request, **kwargs)
        return wrapper
    return decorator
