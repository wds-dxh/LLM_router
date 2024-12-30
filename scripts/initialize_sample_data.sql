

-- 插入基础权限
INSERT INTO permissions (permission_name, description) VALUES
    ('llm.chat', 'LLM对话权限'),
    ('all', '传入音频数据获得大模型对话后的音频'),
    ('conversation.read', '查看对话历史权限'),
    ('conversation.delete', '删除对话历史权限');

-- 插入示例API密钥（与设备ID绑定）
INSERT INTO api_keys (api_key, device_id, description, status) VALUES
    ('sk-test-123456', 'device_001', '测试设备1-完整权限', 'active'),
    ('sk-test-234567', 'device_002', '测试设备2-仅对话', 'active'),
    ('sk-test-345678', 'device_003', '测试设备3-仅语音服务', 'active');

-- 为API密钥分配权限
-- 为第一个API密钥分配所有权限
INSERT INTO api_key_permissions (api_key_id, permission_id)
SELECT 1, id FROM permissions;

-- 为第二个API密钥分配仅对话相关权限
INSERT INTO api_key_permissions (api_key_id, permission_id)
SELECT 2, id FROM permissions WHERE permission_name IN ('llm.chat', 'conversation.read');

-- 为第三个API密钥分配语音服务权限
INSERT INTO api_key_permissions (api_key_id, permission_id)
SELECT 3, id FROM permissions WHERE permission_name IN ('stt.create', 'tts.create');

-- 插入一些示例对话记录
INSERT INTO conversations (device_id, user_id, input_text, response_text, role, mood) VALUES
    ('device_001', 'user_001', '你好，请问现在几点了？', '现在是下午3点整。', 'assistant', 'neutral'),
    ('device_001', 'user_001', '今天天气怎么样？', '根据我获得的信息，今天是晴天，气温适宜。', 'assistant', 'neutral'),
    ('device_002', 'user_002', '帮我写一首诗', '春风拂面暖，花开满园香。\n鸟语声声远，心情格外畅。', 'poet', 'happy');
