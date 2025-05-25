# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
# For prerequisites running the following sample, visit https://help.aliyun.com/zh/model-studio/getting-started/first-api-call-to-qwen
# Paraformer_v2 reference: https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-api
# Language code reference: https://help.aliyun.com/zh/machine-translation/support/supported-languages-and-codes?spm=a2c4g.11186623.0.0.f3b34b8acaDlFM

# standard
import os
import signal  # for keyboard events handling (press "Ctrl+C" to terminate recording)
import sys

# third-party
import dashscope
import pyaudio
from dashscope.audio.asr import Recognition, RecognitionCallback, RecognitionResult
from dotenv import load_dotenv

# custom
from translater import AliTranslator


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


load_dotenv()
init_dashscope_api_key()


# Real-time speech recognition callback
class TranslateCallback(RecognitionCallback):
    def __init__(
        self, from_lang, to_lang, *, sample_rate, channels, block_size, device_name
    ):
        # translator
        self.translator = AliTranslator(
            access_key_id=os.getenv("ALIYUN_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIYUN_ACCESS_KEY_SECRET"),
            endpoint="mt.aliyuncs.com",
            qps=50,
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


# main function
def main():
    init_dashscope_api_key()
    print("Initializing ...")

    # Set recording parameters
    sample_rate = 16000  # sampling rate (Hz)
    channels = 1  # mono channel
    format_pcm = "pcm"  # the format of the audio data
    block_size = 3200  # number of frames per buffer
    from_lang = "jp"
    to_lang = "zh"

    # Create the recognition callback
    callback = TranslateCallback(
        from_lang=from_lang,
        to_lang=to_lang,
        sample_rate=sample_rate,
        channels=channels,
        block_size=block_size,
        device_name="CABLE Output",
    )

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
        language_hints=[from_lang],
    )

    # Start recognition
    recognition.start()

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

    """
    signal库使用参考：
    - https://docs.python.org/zh-cn/3/library/signal.html
    - https://cloud.tencent.com/developer/article/1950657
    常用信号量：
    signal.SIGHUP   # 连接挂断，这个信号的默认操作为终止进程，因此会向终端输出内容的那些进程就会终止。不过有的进程可以捕捉这个信号并忽略它。比如wget。
    signal.SIGINT   # 连接中断，程序终止(interrupt)信号，按下CTRL + C的时候触发。
    signal.SIGTSTP # 暂停进程，停止进程的运行，按下CTRL + Z的时候触发， 该信号可以被处理和忽略。
    signal.SIGCONT # 继续执行，让一个停止(stopped)的进程继续执行。本信号不能被阻塞。
    signal.SIGKILL # 终止进程，用来立即结束程序的运行，本信号无法被阻塞、处理和忽略。
    signal.SIGALRM # 超时警告，时钟定时信号，计算的是实际的时间或时钟时间
    """
    signal.signal(signal.SIGINT, signal_handler)
    print("Press 'Ctrl+C' to stop recording and recognition...")
    # Create a keyboard listener until "Ctrl+C" is pressed

    while True:
        if callback.stream:
            data = callback.stream.read(block_size, exception_on_overflow=False)
            recognition.send_audio_frame(data)
        else:
            break

    recognition.stop()


if __name__ == "__main__":
    main()
