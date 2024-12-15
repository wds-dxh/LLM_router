# 服务层 README

本项目包含以下四个核心服务模块，每个模块独立负责关键功能，为整个系统提供支持。以下详细介绍各服务的功能和方法。

---

## 1. 设备认证服务（`auth_service.py`）

### 功能
用于对设备的身份进行验证并注册到系统中，确保每个设备经过授权才能访问系统资源。

### 方法

#### `__init__(config_path=None)`
- 加载认证服务的配置文件，包括有效的API密钥列表。
- 参数：
  - `config_path` (str): 配置文件的路径，默认为 `config/auth_config.json`。

#### `authenticate_device(device_name: str, api_key: str) -> bool`
- 验证设备名称和对应的API密钥。
- 成功时，将设备注册到数据库。
- 参数：
  - `device_name` (str): 设备名称。
  - `api_key` (str): 设备的API密钥。
- 返回值：
  - `bool`: 验证是否成功。

---

## 2. 大模型服务（`llm_service.py`）

### 功能
调用大型语言模型（LLM）接口，处理文本请求并生成对话响应。

### 方法

#### `__init__()`
- 初始化LLM服务，加载配置文件并创建 `OpenAIAssistant` 实例。

#### `async process_text(device_name: str, text: str, role_type: Optional[str] = None) -> Dict[str, Any]`
- 处理文本输入，生成模型响应。
- 参数：
  - `device_name` (str): 设备名称（用户ID）。
  - `text` (str): 用户输入的文本。
  - `role_type` (Optional[str]): 可选角色类型。
- 返回值：
  - `Dict`: 包含响应文本和状态的字典。

#### `async process_text_stream(device_name: str, text: str, role_type: Optional[str] = None)`
- 流式处理文本输入，逐步返回模型生成的内容。
- 参数：
  - `device_name` (str): 设备名称。
  - `text` (str): 用户输入的文本。
  - `role_type` (Optional[str]): 可选角色类型。
- 返回值：
  - 生成器，返回包含内容片段的字典。

#### `clear_context(device_name: str)`
- 清除指定设备的对话上下文。
- 参数：
  - `device_name` (str): 设备名称。

---

## 3. 语音识别服务（`speech_to_text.py`）

### 功能
通过 WebSocket 接口连接语音识别服务，将音频文件或数据流转换为文本。

### 方法

#### `__init__(config_path=None)`
- 初始化 ASR 客户端，加载配置文件。
- 参数：
  - `config_path` (str): 配置文件路径，默认为 `config/stt_config.json`。

#### `recognize_audio_file(audio_file_path: str) -> str`
- 对指定音频文件进行识别。
- 参数：
  - `audio_file_path` (str): 音频文件路径（支持 `.wav` 和 `.pcm` 格式）。
- 返回值：
  - `str`: 识别出的文本结果。

#### `recognize_audio_stream(pcm_data: bytes) -> str`
- 对原始 PCM 音频数据进行识别。
- 参数：
  - `pcm_data` (bytes): PCM 格式的音频数据。
- 返回值：
  - `str`: 识别出的文本结果。

#### 私有方法（内部使用）
- `_connect()`: 建立与 WebSocket 服务的连接。
- `_send_and_receive(websocket, audio_bytes, wav_name, wav_format)`: 发送音频数据并接收结果。
- `_receive_messages(websocket)`: 从服务端接收识别结果。

---

## 4. 文本转语音服务（`text_to_speech.py`）

### 功能
调用 TTS 服务，将文本转换为音频数据。

### 方法

#### `__init__(config_path=None)`
- 初始化 TTS 服务，加载配置文件。
- 参数：
  - `config_path` (str): 配置文件路径，默认为 `config/tts_config.json`。

#### `synthesize(text: str, user_id: str = "default_user") -> bytes`
- 将文本转换为语音音频数据。
- 参数：
  - `text` (str): 要转换的文本。
  - `user_id` (str): 用户ID，用于标识请求。
- 返回值：
  - `bytes`: 转换后的音频数据。

#### `update_settings(new_settings: Dict[str, Any]) -> None`
- 更新 TTS 服务的设置。
- 参数：
  - `new_settings` (Dict): 包含新设置的字典。

---

## 配置文件路径

各服务的默认配置文件路径如下：
- `auth_config.json`: 配置认证服务的有效API密钥。
- `llm_config.json`: 配置LLM服务的API密钥与相关参数。
- `stt_config.json`: 配置语音识别服务的连接与识别参数。
- `tts_config.json`: 配置文本转语音服务的API连接与语音参数。

---

## 运行方式

1. 确保各服务的配置文件已正确配置。
2. 启动各服务模块，或将其集成到主程序中。
3. 使用测试数据调用各服务方法，验证其功能。

---

## 联系方式

- 作者: wds-Ubuntu22-cqu
- 邮箱: wdsnpshy@163.com
- 日期: 2024-12-15
