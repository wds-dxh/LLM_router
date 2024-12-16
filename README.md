# LLM Router

一个集成了LLM（大语言模型）、STT（语音识别）和TTS（语音合成）的后端框架。

## 功能特点

- 支持多种实现方式：
  - 本地模型实现（本地大模型、本地STT、本地TTS）
  - 第三方API调用

- 多协议支持：
  - WebSocket协议
  - HTTP协议

- 灵活的服务调用：
  - 音频数据处理（STT + LLM + TTS）
  - 直接返回对话结果
  - 单独的STT/TTS/LLM服务调用

- 数据持久化：
  - LLM对话内容存储
  - STT识别结果存储
  - 简单的配置即可启用

- Docker支持：
  - 一键部署（docker-compose）
  - 包含数据库和后端服务

## 项目结构

```
project_root/
├── app/                        # 主应用目录
│   ├── routers/               # 路由目录
│   ├── services/              # 服务逻辑目录
│   ├── utils/                 # 工具模块目录
│   ├── models/                # 数据模型目录
│   ├── middlewares/           # 中间件目录
│   └── tests/                 # 单元测试目录
├── config/                    # 配置文件目录
├── data/                      # 数据文件目录
└── migrations/                # 数据库迁移目录
```

## 快速开始

1. 克隆项目
2. 配置环境变量
3. 使用docker-compose启动服务

## 配置说明

详细配置说明请参考 `config/` 目录下的配置文件。

## API文档

待补充

## 开发说明

待补充

## 许可证

待补充