# -*- encoding: utf-8 -*-
import os
import json
import ssl
import asyncio
import websockets
import logging
import wave
import time

logging.basicConfig(level=logging.ERROR)

class ASRClient:
    """
    ASRClient类用于通过WebSocket连接到语音识别服务，并对音频文件或音频流进行识别。

    参数说明：
    host:       服务器的主机名或IP地址，如"localhost"或"127.0.0.1"
    port:       服务器端口号，如10095
    mode:       识别模式，"offline"、"online"或"2pass"
    chunk_size: 分块大小配置列表, 例如[5,10,5]
                通常用于服务端进行语音分块识别的参数
    chunk_interval: 分块间隔(毫秒)，例如10ms
    hotword:    热词文件的路径，可选。如需使用热词提高特定词的识别率，将文件中每行
                按 "词语 频次" 格式配置
    audio_fs:   音频采样率，默认16000Hz
    use_itn:    是否使用ITN（文本反标准化），1为使用，0为不使用
    ssl:        是否使用SSL加密连接，True或False
    """

    def __init__(self, config_path=None):
        # 加载配置文件
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '../config/stt_config.json')
        
        with open(config_path, 'r') as f:
            config = json.load(f)['asr']
        
        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 10095)
        self.mode = config.get('mode', 'offline')
        self.chunk_size = config.get('chunk_size', [5, 10, 5])
        self.chunk_interval = config.get('chunk_interval', 10)
        self.hotword = config.get('hotword', '')
        self.audio_fs = config.get('audio_fs', 16000)
        self.use_itn = config.get('use_itn', True)
        self.words_max_print = config.get('words_max_print', 10000)
        self.ssl = config.get('ssl', False)
        self.timeout = config.get('timeout', 10)

        # 热词处理
        self.hotword_msg = ""
        if self.hotword.strip():
            fst_dict = {}
            with open(self.hotword, "r", encoding="utf-8") as f_scp:
                hot_lines = f_scp.readlines()
                for line in hot_lines:
                    words = line.strip().split(" ")
                    if len(words) < 2:
                        print("请检查热词文件格式。")
                        continue
                    try:
                        fst_dict[" ".join(words[:-1])] = int(words[-1])
                    except ValueError:
                        print("请检查热词文件格式。")
            self.hotword_msg = json.dumps(fst_dict)

    async def _connect(self):
        """
        内部方法：建立与ASR服务器的WebSocket连接
        """
        if self.ssl:
            ssl_context = ssl.SSLContext()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            uri = f"wss://{self.host}:{self.port}"
        else:
            ssl_context = None
            uri = f"ws://{self.host}:{self.port}"

        websocket = await websockets.connect(uri, subprotocols=["binary"], ping_interval=None, ssl=ssl_context)
        return websocket

    async def _send_and_receive(self, websocket, audio_bytes, wav_name="demo", wav_format="pcm"):
        """
        内部方法：发送音频数据并接收识别结果。
        参数：
        websocket: 已连接的websocket对象
        audio_bytes: 音频数据的字节流 (PCM格式)
        wav_name: 发送给服务端的音频名称标识
        wav_format: 音频格式，如"pcm"或"wav"
        """

        # 构造初始JSON消息，包含模式、分块参数、采样率等信息
        init_msg = json.dumps({
            "mode": self.mode,
            "chunk_size": self.chunk_size,
            "chunk_interval": self.chunk_interval,
            "audio_fs": self.audio_fs,
            "wav_name": wav_name,
            "wav_format": wav_format,
            "is_speaking": True,
            "hotwords": self.hotword_msg,
            "itn": self.use_itn
        })
        await websocket.send(init_msg)

        stride = int((60 * self.chunk_size[1] / self.chunk_interval / 1000) * self.audio_fs * 2)
        if stride == 0:
            stride = 320  # fallback

        chunk_num = (len(audio_bytes) - 1) // stride + 1

        # 异步任务：接收识别结果
        receive_task = asyncio.create_task(self._receive_messages(websocket))
        # 发送音频数据
        for i in range(chunk_num):
            beg = i * stride
            data_chunk = audio_bytes[beg:beg + stride]
            await websocket.send(data_chunk)
            # 最后一块音频发送结束后，告知服务端is_speaking结束
            if i == chunk_num - 1:
                end_msg = json.dumps({"is_speaking": False})    # 把标志设置为is_speaking，表示本段数据识别结束
                await websocket.send(end_msg)

            if self.mode == "offline":
                await asyncio.sleep(0.001)
            else:
                sleep_duration = (60 * self.chunk_size[1] / self.chunk_interval / 1000)
                await asyncio.sleep(sleep_duration)

        # 等待接收任务完成或超时
        try:
            final_result = await asyncio.wait_for(receive_task, timeout=self.timeout)
        except asyncio.TimeoutError:
            print("等待结果超时，返回已获取的部分文本。")
            # 如果超时，则receive_task中已收集到的结果就返回（如果内部逻辑不变，可能为空）
            # 此处可以在 _receive_messages 中使用一个列表来存储最终文本，这里简化为返回空文本。
            final_result = ""

        await websocket.close()
        return final_result

    async def _receive_messages(self, websocket):
        """
        内部方法：从服务端接收识别消息，���到接收最终结果或收到第一条结果后返回。
        如果服务端不返回is_final，可在收到第一条结果后即返回。
        """
        final_text = ""
        first_message_received = False
        try:
            while True:
                msg = await websocket.recv()
                msg = json.loads(msg)
                text = msg.get("text", "")
                is_final = msg.get("is_final", False)
                # 打印接收到的中间结果
                # print("接收到服务端结果: ", text)

                if text:
                    final_text = text
                    first_message_received = True

                # 如果服务端返回is_final为True，表示结果定稿
                if is_final:
                    break

                # 如果服务端没有is_final，但是已接收到文本结果，可以选择立即返回
                # 如果您需要持续接收中间结果，则注释掉下面的break
                if first_message_received and self.mode == "offline":
                    # 若模式为offline且收到首条信息后直接返回（防止卡住）
                    break

        except Exception as e:
            logging.error(f"接收消息出现异常: {e}")
        return final_text

    def recognize_audio_file(self, audio_file_path):
        """
        对指定音频文件进行语音识别。
        支持wav和pcm文件。如果是wav将自动读取wav头并提取数据。
        返回识别出的文本结果字符串。
        """
        # 读取音频文件内容
        if audio_file_path.endswith(".pcm"):
            with open(audio_file_path, "rb") as f:
                audio_bytes = f.read()
            wav_format = "pcm"
            wav_name = os.path.basename(audio_file_path)
        elif audio_file_path.endswith(".wav"):
            with wave.open(audio_file_path, "rb") as wav_file:
                self.audio_fs = wav_file.getframerate()  # 更新实际采样率
                frames = wav_file.readframes(wav_file.getnframes())
                audio_bytes = bytes(frames)
            wav_format = "wav"
            wav_name = os.path.basename(audio_file_path)
        else:
            # 其他格式当作二进制数据处理
            with open(audio_file_path, "rb") as f:
                audio_bytes = f.read()
            wav_format = "others"
            wav_name = os.path.basename(audio_file_path)

        return asyncio.run(self._run_recognition(audio_bytes, wav_name, wav_format))

    def recognize_audio_stream(self, pcm_data):
        """
        对原始PCM音频数据进行识别。
        pcm_data: bytes类型的PCM音频数据，格式应为16kHz单声道16bit。
        返回识别出的文本结果字符串。
        """
        wav_name = "stream_data"
        wav_format = "pcm"
        return asyncio.run(self._run_recognition(pcm_data, wav_name, wav_format))

    async def _run_recognition(self, audio_bytes, wav_name, wav_format):
        """
        内部方法：运行识别流程，包括连接、发送、接收。
        """
        websocket = await self._connect()
        result = await self._send_and_receive(websocket, audio_bytes, wav_name, wav_format)
        return result

