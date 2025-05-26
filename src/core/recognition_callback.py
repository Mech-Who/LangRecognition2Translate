# standard
import os
import sys

# third-party
import pyaudio
from dashscope.audio.asr import RecognitionCallback, RecognitionResult

# custom
from src.core.translater import AliTranslator


# Real-time speech recognition callback
class TranslateCallback(RecognitionCallback):
    def __init__(
        self, from_lang, to_lang, *, sample_rate, channels, block_size, device_name, qps
    ):
        # translator
        self.translator = AliTranslator(
            access_key_id=os.getenv("ALIYUN_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIYUN_ACCESS_KEY_SECRET"),
            endpoint="mt.aliyuncs.com",
            qps=qps,
        )
        # save
        self.stream = None
        self.mic = None
        # config
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.sample_rate = sample_rate
        self.channels = channels
        self.block_size = block_size
        self.device_name = device_name

    def on_open(self) -> None:
        print("RecognitionCallback open.")
        self.mic = pyaudio.PyAudio()
        for i in range(self.mic.get_device_count()):
            dev_info = self.mic.get_device_info_by_index(i)
            # if "CABLE Output" in dev_info["name"]:  # 网页2的虚拟设备标识
            if self.device_name in dev_info["name"]:  # 网页2的虚拟设备标识
                device_index = dev_info["index"]
                break
        else:
            raise Exception("未找到虚拟声卡设备")

        self.stream = self.mic.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=self.block_size,
        )

    def on_close(self) -> None:
        print("RecognitionCallback close.")
        self.stream.stop_stream()
        self.stream.close()
        self.mic.terminate()
        self.stream = None
        self.mic = None

    def on_complete(self) -> None:
        print("RecognitionCallback completed.")  # recognition completed

    def on_error(self, message) -> None:
        print("RecognitionCallback task_id: ", message.request_id)
        print("RecognitionCallback error: ", message.message)
        # Stop and close the audio stream if it is running
        if "stream" in globals() and self.stream.active:
            self.stream.stop()
            self.stream.close()
        # Forcefully exit the program
        sys.exit(1)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if "text" in sentence:
            # print("RecognitionCallback text: ", sentence["text"])
            if RecognitionResult.is_sentence_end(sentence):
                print(
                    "RecognitionCallback sentence end, request_id:%s, usage:%s"
                    % (result.get_request_id(), result.get_usage(sentence))
                )
                response = self.translator.translate(
                    sentence["text"], from_lang=self.from_lang, to_lang=self.to_lang
                )
                # print(response)
                if response.status_code == 200:
                    translate_text = response.body.data.translated
                    print("TranslateText: ", translate_text)
                else:
                    print("Unkown Content:", response)
