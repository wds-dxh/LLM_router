
    "Request": {
        "stt": audio：音频文件（格式：MP3、PCM 等）

        "llm": {
            "role": "user",           // 当前角色：user / assistant
            "input": "今天天气如何？",  // 用户输入文本
            }

        "tts": {
            "text": "你好，这是一段需要合成的文本。", // 需要合成的文本
            "voice": "male"                      // 可选，音色类型：male/female
                }

        "all": {
                "role": "user",           // 当前角色：user / assistant
                "audio": "audio：音频文件（格式：MP3、PCM 等）"
                }
                
    }
    "response":
    {
        "stt": {
            "text": "今天天气晴朗。", // 识别结果
            "confidence": 0.9          // 可选，置信度
            }

        "llm": {
            "role": "assistant",      // 当前角色：user / assistant
            "output": "今天天气晴朗。", // 机器人输出文本
            }

        "tts": {
            "audio": "audio：音频文件（格式：MP3、PCM 等）"
            }

        "all": {
            "audio": "audio：音频文件（格式：MP3、PCM 等）" //大模型对话完成后的音频
            }
    }




