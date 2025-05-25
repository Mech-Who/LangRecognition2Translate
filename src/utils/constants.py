from enum import IntEnum, StrEnum


class Language(StrEnum):
    CHINESE = "zh"
    JAPANESE = "jp"
    KOREAN = "ko"


class BlockSize(IntEnum):
    BS_12800 = 12800
    BS_6400 = 6400
    BS_3200 = 3200
    BS_1600 = 1600
    BS_800 = 800


class SampleRate(IntEnum):
    SR_48000 = 48000
    SR_44100 = 44100
    SR_24000 = 24000
    SR_22050 = 22050
    SR_16000 = 16000
    SR_11025 = 11025


class VoiseChannels(IntEnum):
    CHANNEL_STEREO = 1
    CHANNEL_MONO = 2
