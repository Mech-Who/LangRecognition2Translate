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
from dashscope.audio.asr import Recognition
from dotenv import load_dotenv

from src.core.recognition_callback import TranslateCallback
from src.utils.config import config

# custom
from src.utils.constants import BlockSize, Format, Language, SampleRate, VoiceChannel


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


# main function
def main():
    load_dotenv()
    init_dashscope_api_key()
    print("Initializing ...")

    # Set recording parameters
    channels = VoiceChannel.from_string(
        config["recognition"]["voice_channel"]
    )  # mono channel
    format_pcm = Format.from_string(
        config["recognition"]["data_format"]
    )  # the format of the audio data
    sample_rate = SampleRate.from_int(
        config["recognition"]["sample_rate"]
    )  # sampling rate (Hz)
    block_size = BlockSize.from_int(
        config["recognition"]["block_size"]
    )  # number of frames per buffer
    from_lang = Language.from_string(config["general"]["from_lang"])
    to_lang = Language.from_string(config["general"]["to_lang"])
    qps = config["translation"]["qps"]

    # Create the recognition callback
    callback = TranslateCallback(
        from_lang=from_lang,
        to_lang=to_lang,
        sample_rate=sample_rate,
        channels=channels,
        block_size=block_size,
        device_name="CABLE Output",
        qps=qps,
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
