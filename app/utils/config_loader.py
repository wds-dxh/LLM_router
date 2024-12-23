import json
import os
from typing import Dict, Any

import sys
sys.path.append("/home/wds/workspace/now/LLM_router")
# print(sys.path)

class ConfigLoader:
    """
    负责加载配置文件，为 STT、TTS 和 LLM 提供配置支持。
    """

    def __init__(self, config_directory: str = "config"):
        """
        初始化 ConfigLoader，指定配置文件目录。
        默认目录为 `config`。
        """
        self.config_directory = config_directory
        self.config = self._load_all_configs()
        self._process_paths()

    def _process_paths(self) -> None:
        """处理配置文件中的路径，转换为绝对路径"""
        for service_type in ["stt", "llm"]:  # 处理所有服务类型的路径
            if service_type in self.config:
                storage = self.config[service_type].get("storage", {})
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                
                for key in ["conversations_path", "prompts_path"]:
                    if key in storage:
                        if not os.path.isabs(storage[key]):
                            storage[key] = os.path.join(base_dir, storage[key])
                        # 确保目录存在
                        os.makedirs(os.path.dirname(storage[key]), exist_ok=True)

    def _load_all_configs(self):
        """
        加载所有配置文件（STT, TTS, LLM）。
        """
        configs = {
            "stt": self._load_config("stt_config.json"),
            "llm": self._load_config("llm_config.json"),  # 添加LLM配置
            # "tts": self._load_config("tts_config.json")
        }
        return configs

    def _load_config(self, config_file: str):
        """
        加载单个配置文件。
        """
        config_path = os.path.join(self.config_directory, config_file)
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file {config_file} not found.")

        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_stt_config(self):
        """
        获取 STT 配置。
        """
        return self.config.get("stt")

    def get_tts_config(self):
        """
        获取 TTS 配置。
        """
        return self.config.get("tts")

    def get_llm_config(self) -> Dict:
        """
        获取LLM配置，返回完整配置包括公共部分
        """
        if "llm" not in self.config:
            return None
            
        # 返回完整配置，包括providers、storage等所有内容
        return self.config["llm"]

    def get_provider_config(self, service_type: str, provider_name: str):
        """
        根据服务类型和提供商名称获取相应的配置。
        同时合并公共配置（storage、conversation等）
        """
        if service_type not in self.config:
            raise ValueError(f"Unknown service type: {service_type}")
        
        service_config = self.config[service_type]
        provider_config = service_config.get("providers", {}).get(provider_name)
        
        if not provider_config:
            raise ValueError(f"Provider {provider_name} not found in {service_type} config.")
        
        # 合并公共配置
        merged_config = provider_config.copy()
        
        # 添加存储配置
        if "storage" in service_config:
            merged_config["storage"] = service_config["storage"]
            
        # 添加对话配置
        if "conversation" in service_config:
            merged_config["conversation"] = service_config["conversation"]
            
        return merged_config

    def get_default_provider(self, service_type: str):
        """
        获取服务类型的默认提供商。
        """
        if service_type not in self.config:
            raise ValueError(f"Unknown service type: {service_type}")
        
        return self.config[service_type].get("default_provider")


if __name__ == "__main__":
    config_loader = ConfigLoader()
    print(config_loader.get_llm_config())

    # print(config_loader.get_provider_config("stt", "aliyun").get("api_key"))