## 使用示例

### ApiKeyModel

**描述**: 管理API Key的模型。

**方法**:
- `create(**kwargs) -> Dict[str, Any]`: 创建API Key记录。
    ```python
    new_api_key = ApiKeyModel.create(name="example_key", key="123456")
    ```
- `get_by_id(id: int) -> Optional[Dict[str, Any]]`: 通过ID获取API Key记录。
    ```python
    api_key = ApiKeyModel.get_by_id(1)
    ```
- `get_all(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]`: 获取所有API Key记录。
    ```python
    api_keys = ApiKeyModel.get_all(limit=50, offset=0)
    ```
- `update(id: int, **kwargs) -> bool`: 更新API Key记录。
    ```python
    success = ApiKeyModel.update(1, name="updated_key")
    ```
- `delete(id: int) -> bool`: 删除API Key记录。
    ```python
    success = ApiKeyModel.delete(1)
    ```

### PermissionModel

**描述**: 管理权限的模型。

**方法**:
- `create(**kwargs) -> Dict[str, Any]`: 创建权限记录。
    - 参数:
        - `**kwargs`: 权限的属性，例如`name`。
    - 返回值: 包含新创建的权限记录的字典。
    ```python
    new_permission = PermissionModel.create(name="read_access")
    ```
- `get_by_id(id: int) -> Optional[Dict[str, Any]]`: 通过ID获取权限记录。
    - 参数:
        - `id`: 权限的ID。
    - 返回值: 包含权限记录的字典，如果未找到则返回`None`。
    ```python
    permission = PermissionModel.get_by_id(1)
    ```
- `get_all(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]`: 获取所有权限记录。
    - 参数:
        - `limit`: 返回记录的最大数量。
        - `offset`: 记录的偏移量。
    - 返回值: 包含权限记录的字典列表。
    ```python
    permissions = PermissionModel.get_all(limit=50, offset=0)
    ```
- `update(id: int, **kwargs) -> bool`: 更新权限记录。
    - 参数:
        - `id`: 权限的ID。
        - `**kwargs`: 要更新的权限属性。
    - 返回值: 更新是否成功的布尔值。
    ```python
    success = PermissionModel.update(1, name="write_access")
    ```
- `delete(id: int) -> bool`: 删除权限记录。
    - 参数:
        - `id`: 权限的ID。
    - 返回值: 删除是否成功的布尔值。
    ```python
    success = PermissionModel.delete(1)
    ```
- `get_by_name(permission_name: str) -> Optional[Dict[str, Any]]`: 通过权限名称获取权限记录。
    - 参数:
        - `permission_name`: 权限的名称。
    - 返回值: 包含权限记录的字典，如果未找到则返回`None`。
    ```python
    permission = PermissionModel.get_by_name("read_access")
    ```
- `get_api_keys_with_permission(permission_name: str) -> List[Dict[str, Any]]`: 获取拥有指定权限的所有API Key。
    - 参数:
        - `permission_name`: 权限的名称。
    - 返回值: 包含API Key记录的字典列表。
    ```python
    api_keys = PermissionModel.get_api_keys_with_permission("read_access")
    ```

### ConversationModel

**描述**: 管理对话记录的模型。

**方法**:
- `create(**kwargs) -> Dict[str, Any]`: 创建对话记录。
    ```python
    new_conversation = ConversationModel.create(user_id="user123", content="Hello, world!")
    ```
- `get_by_id(id: int) -> Optional[Dict[str, Any]]`: 通过ID获取对话记录。
    ```python
    conversation = ConversationModel.get_by_id(1)
    ```
- `get_all(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]`: 获取所有对话记录。
    ```python
    conversations = ConversationModel.get_all(limit=50, offset=0)
    ```
- `update(id: int, **kwargs) -> bool`: 更新对话记录。
    ```python
    success = ConversationModel.update(1, content="Updated content")
    ```
- `delete(id: int) -> bool`: 删除对话记录。
    ```python
    success = ConversationModel.delete(1)
    ```
- `search_conversations(keyword: str, device_id: str = None, user_id: str = None, start_date: datetime = None, end_date: datetime = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]`: 搜索对话记录。
    ```python
    results = ConversationModel.search_conversations(keyword="hello", user_id="user123")
    ```
- `get_by_device_id(device_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]`: 获取指定设备的对话记录。
    ```python
    conversations = ConversationModel.get_by_device_id("device123", limit=50, offset=0)
    ```

### STTResultModel

**描述**: 管理语音识别结果的模型。

**方法**:
- `create(**kwargs) -> Dict[str, Any]`: 创建语音识别记录。
    - 参数:
        - `**kwargs`: 语音识别的属性，例如`device_id`和`result`。
    - 返回值: 包含新创建的语音识别记录的字典。
    ```python
    new_stt_result = STTResultModel.create(device_id="device123", result="Hello, world!")
    ```
- `get_by_id(id: int) -> Optional[Dict[str, Any]]`: 通过ID获取语音识别记录。
    - 参数:
        - `id`: 语音识别记录的ID。
    - 返回值: 包含语音识别记录的字典，如果未找到则返回`None`。
    ```python
    stt_result = STTResultModel.get_by_id(1)
    ```
- `get_all(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]`: 获取所有语音识别记录。
    - 参数:
        - `limit`: 返回记录的最大数量。
        - `offset`: 记录的偏移量。
    - 返回值: 包含语音识别记录的字典列表。
    ```python
    stt_results = STTResultModel.get_all(limit=50, offset=0)
    ```
- `update(id: int, **kwargs) -> bool`: 更新语音识别记录。
    - 参数:
        - `id`: 语音识别记录的ID。
        - `**kwargs`: 要更新的语音识别属性。
    - 返回值: 更新是否成功的布尔值。
    ```python
    success = STTResultModel.update(1, result="Updated result")
    ```
- `delete(id: int) -> bool`: 删除语音识别记录。
    - 参数:
        - `id`: 语音识别记录的ID。
    - 返回值: 删除是否成功的布尔值。
    ```python
    success = STTResultModel.delete(1)
    ```
- `search_results(keyword: str, device_id: str = None, start_date: datetime = None, end_date: datetime = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]`: 搜索语音识别记录。
    - 参数:
        - `keyword`: 搜索关键字。
        - `device_id`: 设备ID（可选）。
        - `start_date`: 开始日期（可选）。
        - `end_date`: 结束日期（可选）。
        - `limit`: 返回记录的最大数量。
        - `offset`: 记录的偏移量。
    - 返回值: 包含语音识别记录的字典列表。
    ```python
    results = STTResultModel.search_results(keyword="hello", device_id="device123")
    ```
- `get_by_device_id(device_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]`: 获取指定设备的语音识别记录。
    - 参数:
        - `device_id`: 设备ID。
        - `limit`: 返回记录的最大数量。
        - `offset`: 记录的偏移量。
    - 返回值: 包含语音识别记录的字典列表。
    ```python
    stt_results = STTResultModel.get_by_device_id("device123", limit=50, offset=0)
    ```
- `get_by_file_path(audio_file_path: str) -> Optional[Dict[str, Any]]`: 通过音频文件路径获取语音识别记录。
    - 参数:
        - `audio_file_path`: 音频文件路径。
    - 返回值: 包含语音识别记录的字典，如果未找到则返回`None`。
    ```python
    stt_result = STTResultModel.get_by_file_path("/path/to/audio/file")
    ```
- `delete_by_device_id(device_id: str) -> bool`: 删除指定设备的所有语音识别记录。
    - 参数:
        - `device_id`: 设备ID。
    - 返回值: 删除是否成功的布尔值。
    ```python
    success = STTResultModel.delete_by_device_id("device123")
    ```

### TTSResultModel

**描述**: 管理语音合成结果的模型。

**方法**:
- `create(**kwargs) -> Dict[str, Any]`: 创建语音合成记录。
    ```python
    new_tts_result = TTSResultModel.create(device_id="device123", result="Synthesized speech")
    ```
- `get_by_id(id: int) -> Optional[Dict[str, Any]]`: 通过ID获取语音合成记录。
    ```python
    tts_result = TTSResultModel.get_by_id(1)
    ```
- `get_all(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]`: 获取所有语音合成记录。
    ```python
    tts_results = TTSResultModel.get_all(limit=50, offset=0)
    ```
- `update(id: int, **kwargs) -> bool`: 更新语音合成记录。
    ```python
    success = TTSResultModel.update(1, result="Updated synthesized speech")
    ```
- `delete(id: int) -> bool`: 删除语音合成记录。
    ```python
    success = TTSResultModel.delete(1)
    ```
- `search_results(keyword: str, device_id: str = None, start_date: datetime = None, end_date: datetime = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]`: 搜索语音合成记录。
    ```python
    results = TTSResultModel.search_results(keyword="hello", device_id="device123")
    ```
- `get_by_device_id(device_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]`: 获取指定设备的语音合成记录。
    ```python
    tts_results = TTSResultModel.get_by_device_id("device123", limit=50, offset=0)
    ```
- `get_by_file_path(audio_file_path: str) -> Optional[Dict[str, Any]]`: 通过音频文件路径获取语音合成记录。
    ```python
    tts_result = TTSResultModel.get_by_file_path("/path/to/audio/file")
    ```
- `delete_by_device_id(device_id: str) -> bool`: 删除指定设备的所有语音合成记录。
    ```python
    success = TTSResultModel.delete_by_device_id("device123")
    ```
- `get_by_input_text(input_text: str) -> Optional[Dict[str, Any]]`: 通过输入文本获取语音合成记录。
    ```python
        tts_result = TTSResultModel.get_by_input_text("Hello, world!")
    ```

    ## 使用示例

    ### ApiKeyModel 使用示例

    ```python
    # 创建API Key
    new_api_key = ApiKeyModel.create(name="example_key", key="123456")

    # 通过ID获取API Key
    api_key = ApiKeyModel.get_by_id(1)

    # 获取所有API Key
    api_keys = ApiKeyModel.get_all(limit=50, offset=0)

    # 更新API Key
    success = ApiKeyModel.update(1, name="updated_key")

    # 删除API Key
    success = ApiKeyModel.delete(1)
    ```

    ### PermissionModel 使用示例

    ```python
    # 创建权限
    new_permission = PermissionModel.create(name="read_access")

    # 通过ID获取权限
    permission = PermissionModel.get_by_id(1)

    # 获取所有权限
    permissions = PermissionModel.get_all(limit=50, offset=0)

    # 更新权限
    success = PermissionModel.update(1, name="write_access")

    # 删除权限
    success = PermissionModel.delete(1)

    # 通过权限名称获取权限
    permission = PermissionModel.get_by_name("read_access")

    # 获取拥有指定权限的所有API Key
    api_keys = PermissionModel.get_api_keys_with_permission("read_access")
    ```

    ### ConversationModel 使用示例

    ```python
    # 创建对话记录
    new_conversation = ConversationModel.create(user_id="user123", content="Hello, world!")

    # 通过ID获取对话记录
    conversation = ConversationModel.get_by_id(1)

    # 获取所有对话记录
    conversations = ConversationModel.get_all(limit=50, offset=0)

    # 更新对话记录
    success = ConversationModel.update(1, content="Updated content")

    # 删除对话记录
    success = ConversationModel.delete(1)

    # 搜索对话记录
    results = ConversationModel.search_conversations(keyword="hello", user_id="user123")

    # 获取指定设备的对话记录
    conversations = ConversationModel.get_by_device_id("device123", limit=50, offset=0)
    ```

    ### STTResultModel 使用示例

    ```python
    # 创建语音识别记录
    new_stt_result = STTResultModel.create(device_id="device123", result="Hello, world!")

    # 通过ID获取语音识别记录
    stt_result = STTResultModel.get_by_id(1)

    # 获取所有语音识别记录
    stt_results = STTResultModel.get_all(limit=50, offset=0)

    # 更新语音识别记录
    success = STTResultModel.update(1, result="Updated result")

    # 删除语音识别记录
    success = STTResultModel.delete(1)

    # 搜索语音识别记录
    results = STTResultModel.search_results(keyword="hello", device_id="device123")

    # 获取指定设备的语音识别记录
    stt_results = STTResultModel.get_by_device_id("device123", limit=50, offset=0)

    # 通过音频文件路径获取语音识别记录
    stt_result = STTResultModel.get_by_file_path("/path/to/audio/file")

    # 删除指定设备的所有语音识别记录
    success = STTResultModel.delete_by_device_id("device123")
    ```

    ### TTSResultModel 使用示例

    ```python
    # 创建语音合成记录
    new_tts_result = TTSResultModel.create(device_id="device123", result="Synthesized speech")

    # 通过ID获取语音合成记录
    tts_result = TTSResultModel.get_by_id(1)

    # 获取所有语音合成记录
    tts_results = TTSResultModel.get_all(limit=50, offset=0)

    # 更新语音合成记录
    success = TTSResultModel.update(1, result="Updated synthesized speech")

    # 删除语音合成记录
    success = TTSResultModel.delete(1)

    # 搜索语音合成记录
    results = TTSResultModel.search_results(keyword="hello", device_id="device123")

    # 获取指定设备的语音合成记录
    tts_results = TTSResultModel.get_by_device_id("device123", limit=50, offset=0)

    # 通过音频文件路径获取语音合成记录
    tts_result = TTSResultModel.get_by_file_path("/path/to/audio/file")

    # 删除指定设备的所有语音合成记录
    success = TTSResultModel.delete_by_device_id("device123")

    # 通过输入文本获取语音合成记录
    tts_result = TTSResultModel.get_by_input_text("Hello, world!")
    ```