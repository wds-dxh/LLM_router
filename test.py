'''
Author: wds-Ubuntu22-cqu wdsnpshy@163.com
Date: 2024-12-13 01:01:52
Description: 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-Ubuntu22-cqu}, All Rights Reserved. 
'''
#coding=utf-8

'''
requires Python 3.6 or later
pip install requests
'''
import base64
import json
import time
import uuid
import requests

# 填写平台申请的appid, access_token以及cluster
appid = "5407974323"
access_token= "R5Hqb1f_7gD-87aJzStv8vEvBSGG7j_A"
cluster = "volcano_tts"

voice_type = "BV005_streaming"
host = "openspeech.bytedance.com"
api_url = f"https://{host}/api/v1/tts"

header = {"Authorization": f"Bearer;{access_token}"}

request_json = {
    "app": {
        "appid": appid,
        "token": "access_token",
        "cluster": cluster
    },
    "user": {
        "uid": "388808087185088"
    },
    "audio": {
        "voice_type": voice_type,
        "encoding": "mp3",
        "speed_ratio": 1.0,
        "volume_ratio": 1.0,
        "pitch_ratio": 1.0,
    },
    "request": {
        "reqid": str(uuid.uuid4()),
        "text": "字节跳动语音合成字节跳动语音合成字节跳动语音合成字节跳动语音合成字节跳动语音合成字节跳动语音合成字节跳动语音合成字节跳动语音合成",
        "text_type": "plain",
        "operation": "query",
        "with_frontend": 1,
        "frontend_type": "unitTson"

    }
}

if __name__ == '__main__':
    try:
        time_now = time.time()
        resp = requests.post(api_url, json.dumps(request_json), headers=header)
        end_time = time.time()
        

        print(f"resp body: \n{resp.json()}")
        if "data" in resp.json():
            data = resp.json()["data"]  
            file_to_save = open("test_submit.mp3", "wb")
            file_to_save.write(base64.b64decode(data))
        print("总耗时:", end_time - time_now)
    

    except Exception as e:
        e.with_traceback()
    