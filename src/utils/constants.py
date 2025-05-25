from enum import IntEnum, StrEnum


class EnumValueError(Exception):
    def __init__(self, enum_value):
        super().__init__(enum_value)
        self.enum_value = enum_value

    def __str__(self):
        return f"[EnumValueError] Unknown enum value '{self.enum_value}'!"


class Language(StrEnum):
    """Language codes"""

    CHINESE = "zh"
    JAPANESE = "jp"
    KOREAN = "ko"
    ENGLISH = "en"

    @staticmethod
    def from_string(value: str):
        match value:
            case "zh":
                return Language.CHINESE
            case "en":
                return Language.ENGLISH
            case "jp":
                return Language.JAPANESE
            case "ko":
                return Language.KOREAN
            case _:
                raise EnumValueError(value)


class Format(StrEnum):
    """The format of the audio data"""

    F_PCM = "pcm"
    F_WAV = "wav"
    F_OPUS = "opus"
    F_SPEEX = "speex"
    F_AAC = "aac"
    F_AMR = "amr"

    @staticmethod
    def from_string(value: str):
        if value in ["pcm", "wav", "opus", "speex", "aac", "amr"]:
            return eval(f"Format.F_{value.upper()}")
        else:
            raise EnumValueError(value)


class BlockSize(IntEnum):
    """Block size of the audio data"""

    BS_12800 = 12800
    BS_6400 = 6400
    BS_3200 = 3200
    BS_1600 = 1600
    BS_800 = 800

    @staticmethod
    def from_int(value: int):
        if value in [12800, 6400, 3200, 1600, 800]:
            return eval(f"BlockSize.BS_{value}")
        else:
            raise EnumValueError(value)


class SampleRate(IntEnum):
    """The sample rate of audio data"""

    SR_48000 = 48000
    SR_44100 = 44100
    SR_24000 = 24000
    SR_22050 = 22050
    SR_16000 = 16000
    SR_11025 = 11025

    @staticmethod
    def from_int(value: int):
        if value in [48000, 44100, 24000, 22050, 16000, 11025]:
            return eval(f"SampleRate.SR_{value}")
        else:
            raise EnumValueError(value)


class VoiceChannel(IntEnum):
    """Channel num of the audio data"""

    CHANNEL_STEREO = 1
    CHANNEL_MONO = 2

    @staticmethod
    def from_string(value: str):
        match value:
            case "stereo":
                return VoiceChannel.CHANNEL_STEREO
            case "mono":
                return VoiceChannel.CHANNEL_MONO
            case _:
                raise EnumValueError(value)


if __name__ == "__main__":
    print("Running 'src.utils.constants.py'!")
