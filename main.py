# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html

import os

from dashscope.audio.asr import Recognition
from dotenv import load_dotenv

# 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
# import dashscope
# dashscope.api_key = "apiKey"
load_dotenv()


# For prerequisites running the following sample, visit https://help.aliyun.com/zh/model-studio/getting-started/first-api-call-to-qwen
import signal  # for keyboard events handling (press "Ctrl+C" to terminate recording)
import sys

import dashscope
import pyaudio
from dashscope.audio.asr import *

from translater import AliTranslator

mic = None
stream = None

# Set recording parameters
sample_rate = 16000  # sampling rate (Hz)
channels = 1  # mono channel
dtype = "int16"  # data type
format_pcm = "pcm"  # the format of the audio data
block_size = 3200  # number of frames per buffer

translator = AliTranslator(
    access_key_id=os.getenv("ALIYUN_ACCESS_KEY_ID"),
    access_key_secret=os.getenv("ALIYUN_ACCESS_KEY_SECRET"),
    endpoint="mt.aliyuncs.com",
    qps=50,
)


def init_dashscope_api_key():
    """
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if "DASHSCOPE_API_KEY" in os.environ:
        dashscope.api_key = os.environ[
            "DASHSCOPE_API_KEY"
        ]  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = "<your-dashscope-api-key>"  # set API-key manually


# Real-time speech recognition callback
class Callback(RecognitionCallback):
    def on_open(self) -> None:
        global mic
        global stream
        print("RecognitionCallback open.")
        mic = pyaudio.PyAudio()
        for i in range(mic.get_device_count()):
            dev_info = mic.get_device_info_by_index(i)
            if "CABLE Output" in dev_info["name"]:  # 网页2的虚拟设备标识
                device_index = dev_info["index"]
                break
        else:
            raise Exception("未找到虚拟声卡设备")
        stream = mic.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=sample_rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=block_size,
        )

    def on_close(self) -> None:
        global mic
        global stream
        print("RecognitionCallback close.")
        stream.stop_stream()
        stream.close()
        mic.terminate()
        stream = None
        mic = None

    def on_complete(self) -> None:
        print("RecognitionCallback completed.")  # recognition completed

    def on_error(self, message) -> None:
        print("RecognitionCallback task_id: ", message.request_id)
        print("RecognitionCallback error: ", message.message)
        # Stop and close the audio stream if it is running
        if "stream" in globals() and stream.active:
            stream.stop()
            stream.close()
        # Forcefully exit the program
        sys.exit(1)

    def on_event(self, result: RecognitionResult) -> None:
        global translator
        sentence = result.get_sentence()
        if "text" in sentence:
            # print("RecognitionCallback text: ", sentence["text"])
            if RecognitionResult.is_sentence_end(sentence):
                print(
                    "RecognitionCallback sentence end, request_id:%s, usage:%s"
                    % (result.get_request_id(), result.get_usage(sentence))
                )
                response = translator.translate(
                    sentence["text"], from_lang="ko", to_lang="zh"
                )
                # print(response)
                if response.status_code == 200:
                    translate_text = response.body.data.translated
                    print("TranslateText: ", translate_text)
                else:
                    print("Unkown Content:", response)


def signal_handler(sig, frame):
    print("Ctrl+C pressed, stop recognition ...")
    # Stop recognition
    recognition.stop()
    print("Recognition stopped.")
    print(
        "[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}".format(
            recognition.get_last_request_id(),
            recognition.get_first_package_delay(),
            recognition.get_last_package_delay(),
        )
    )
    # Forcefully exit the program
    sys.exit(0)


# main function
def main():
    init_dashscope_api_key()
    print("Initializing ...")

    # Create the recognition callback
    callback = Callback()

    # Call recognition service by async mode, you can customize the recognition parameters, like model, format,
    # sample_rate For more information, please refer to https://help.aliyun.com/document_detail/2712536.html
    recognition = Recognition(
        model="paraformer-realtime-v2",
        # 'paraformer-realtime-v1'、'paraformer-realtime-8k-v1'
        format=format_pcm,
        # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
        sample_rate=sample_rate,
        # support 8000, 16000
        semantic_punctuation_enabled=False,
        callback=callback,
        language_hints=["ko"],
    )

    # Start recognition
    recognition.start()

    signal.signal(signal.SIGINT, signal_handler)
    print("Press 'Ctrl+C' to stop recording and recognition...")
    # Create a keyboard listener until "Ctrl+C" is pressed

    while True:
        if stream:
            data = stream.read(block_size, exception_on_overflow=False)
            recognition.send_audio_frame(data)
        else:
            break

    recognition.stop()


if __name__ == "__main__":
    main()
