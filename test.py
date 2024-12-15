from vosk import Model, KaldiRecognizer # pip install vosk
import wave

# 加载模型
model = Model("model")
recognizer = KaldiRecognizer(model, 16000)  # 16000是采样率

# 接收 PCM 数据流
with wave.open("input.pcm", "rb") as wf:
    while True:
        data = wf.readframes(4000)  # 每次读取一定量的帧
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            print(recognizer.Result())
        else:
            print(recognizer.PartialResult())
