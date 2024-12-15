import json
import os
import sys

from utils.database import add_device

class AuthService:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '../config/auth_config.json')
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.valid_keys = self.config['valid_keys']

    def authenticate_device(self, device_name: str, api_key: str) -> bool:
        """
        验证设备并注册到数据库
        Args:
            device_name: 设备名称
            api_key: 设备的API密钥
        Returns:
            bool: 验证是否成功
        """
        if api_key in self.valid_keys:
            add_device(device_name, api_key)
            return True
        else:
            print(f"设备 {device_name} 验证失败，密钥无效。")
            return False

if __name__ == "__main__":
    auth_service = AuthService()
    print(auth_service.authenticate_device("test_device", "test_key"))
