/*
 * @Author: wds-Ubuntu22-cqu wdsnpshy@163.com
 * @Date: 2024-12-17 07:08:14
 * @Description: 初始化示例数据
 * 邮箱：wdsnpshy@163.com 
 * Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
 */

-- 插入基础权限
INSERT INTO permissions (permission_name, description) VALUES
    ('stt.create', '语音识别权限'),
    ('tts.create', '语音合成权限'),
    ('llm.chat', 'LLM对话权限'),
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
INSERT INTO conversations (device_id, user_id, input_text, response_text, role) VALUES
    ('device_001', 'user_001', '你好，请问现在几点了？', '现在是下午3点整。', 'assistant'),
    ('device_001', 'user_001', '今天天气怎么样？', '根据我获得的信息，今天是晴天，气温适宜。', 'assistant'),
    ('device_002', 'user_002', '帮我写一首诗', '春风拂面暖，花开满园香。\n鸟语声声远，心情格外畅。', 'poet');

-- 插入示例语音识别记录
INSERT INTO stt_results (device_id, audio_file_path, recognized_text) VALUES
    ('device_001', '/audio/input/123.wav', '你好，请问现在几点了？'),
    ('device_002', '/audio/input/456.wav', '今天天气真不错');

-- 插入示例语音合成记录
INSERT INTO tts_results (device_id, input_text, audio_file_path) VALUES
    ('device_001', '现在是下午3点整。', '/audio/output/123.wav'),
    ('device_002', '今天是晴天，气温适宜。', '/audio/output/456.wav');
