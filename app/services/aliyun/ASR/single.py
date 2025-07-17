import time
import threading
import sys
import nls
import json

URL="wss://nls-gateway-cn-shanghai.aliyuncs.com/ws/v1"
TOKEN="8c99bb300db8429b98e67ca97590986e"   #参考https://help.aliyun.com/document_detail/450255.html获取token
APPKEY="shDZg8nfPpbGGO3R"      #获取Appkey请前往控制台：https://nls-portal.console.aliyun.com/applist

class AliRecognizer:
    def __init__(self, audio_data: bytes):
        self.audio_data = audio_data
        self.result_text = ""
        self.finished = threading.Event()

    def test_on_start(self, message, *args):
        print("识别开始")

    def test_on_error(self, message, *args):
        print("识别错误", message)
        self.finished.set()

    def test_on_close(self, *args):
        print("连接关闭")

    def test_on_result_chg(self, message, *args):
        print("中间结果", message)

    def test_on_completed(self, message, *args):
        print("识别完成:", message)
        try:
            msg = json.loads(message)  # <- 加这一步
            self.result_text = msg['payload']['result']
        except Exception as e:
            print("解析识别结果失败:", e)
            self.result_text = ''
        self.finished.set()

    def recognize(self):
        sr = nls.NlsSpeechRecognizer(
            url=URL,
            token=TOKEN,
            appkey=APPKEY,
            on_start=self.test_on_start,
            on_result_changed=self.test_on_result_chg,
            on_completed=self.test_on_completed,
            on_error=self.test_on_error,
            on_close=self.test_on_close,
        )
        sr.start(aformat="pcm")
        for i in zip(*(iter(self.audio_data),) * 640):
            sr.send_audio(bytes(i))
            time.sleep(0.01)
        sr.stop()
        self.finished.wait(timeout=10)  # 最多等待10秒
        return self.result_text