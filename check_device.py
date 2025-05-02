import pyaudio
import sounddevice as sd

print(sd)


# 新增设备检测代码（参考网页1）
def check_devices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"Index {i}: {info['name']} (InputCh: {info['maxInputChannels']})")
