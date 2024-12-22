
import json
import os

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

    def _load_all_configs(self):
        """
        加载所有配置文件（STT, TTS, LLM）。
        """
        configs = {
            "stt": self._load_config("stt_config.json"),
            # "tts": self._load_config("tts_config.json"),
            # "llm": self._load_config("llm_config.json")
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

    def get_llm_config(self):
        """
        获取 LLM 配置。
        """
        return self.config.get("llm")

    def get_provider_config(self, service_type: str, provider_name: str):
        """
        根据服务类型和提供商名称获取相应的配置。
        """
        if service_type not in self.config:
            raise ValueError(f"Unknown service type: {service_type}")
        
        provider_config = self.config[service_type].get("providers", {}).get(provider_name)
        if not provider_config:
            raise ValueError(f"Provider {provider_name} not found in {service_type} config.")
        return provider_config

    def get_default_provider(self, service_type: str):
        """
        获取服务类型的默认提供商。
        """
        if service_type not in self.config:
            raise ValueError(f"Unknown service type: {service_type}")
        
        return self.config[service_type].get("default_provider")


if __name__ == "__main__":
    config_loader = ConfigLoader()
    print(config_loader.get_stt_config())

    print(config_loader.get_provider_config("stt", "aliyun").get("api_key"))