/*
 * @Author: wds-Ubuntu22-cqu wdsnpshy@163.com
 * @Date: 2024-12-17 05:42:36
 * @Description: 初始化数据库
 * 邮箱：wdsnpshy@163.com 
 * Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
 */

-- 创建对话记录表
CREATE TABLE IF NOT EXISTS conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(64),  -- 设备ID，预设的设备标识符
    user_id VARCHAR(64),    -- 用户ID
    input_text TEXT,        -- 输入文本
    response_text TEXT,     -- 响应文本
    role VARCHAR(64),       -- 大模型扮演的角色
    mood VARCHAR(64) DEFAULT 'neutral', -- 对话心情
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建 API Key 表
CREATE TABLE IF NOT EXISTS api_keys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    api_key VARCHAR(64) UNIQUE NOT NULL,    -- API密钥
    device_id VARCHAR(64) NOT NULL,         -- 设备ID，预设的设备标识符
    description VARCHAR(255),               -- 描述
    status ENUM('active', 'inactive') DEFAULT 'active',  -- 状态
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_used_at DATETIME
);

-- 创建权限表
CREATE TABLE IF NOT EXISTS permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    permission_name VARCHAR(64) UNIQUE NOT NULL,  -- 权限名称
    description VARCHAR(255)                      -- 权限描述
);

-- 创建 API Key 权限映射表
CREATE TABLE IF NOT EXISTS api_key_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    api_key_id INT NOT NULL,                -- API Key ID
    permission_id INT NOT NULL,             -- 权限ID
    FOREIGN KEY (api_key_id) REFERENCES api_keys(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
);
