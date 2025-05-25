# 暂时只能通过sys.path完成，没找到其他方案
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.utils.constants import (
    BlockSize,
    Format,
    Language,
    SampleRate,
    VoiceChannel,
)


def test_language():
    # Language "zh", "en", "jp", "ko"
    assert Language.from_string("zh") == Language.CHINESE, "Language enum error!"
    assert Language.from_string("en") == Language.ENGLISH, "Language enum error!"
    assert Language.from_string("jp") == Language.JAPANESE, "Language enum error!"
    assert Language.from_string("ko") == Language.KOREAN, "Language enum error!"


def test_format():
    # Format "pcm", "wav", "opus", "speex", "aac", "amr"
    assert Format.from_string("pcm") == Format.F_PCM, "Format enum error!"
    assert Format.from_string("wav") == Format.F_WAV, "Format enum error!"
    assert Format.from_string("opus") == Format.F_OPUS, "Format enum error!"
    assert Format.from_string("speex") == Format.F_SPEEX, "Format enum error!"
    assert Format.from_string("aac") == Format.F_AAC, "Format enum error!"
    assert Format.from_string("amr") == Format.F_AMR, "Format enum error!"


def test_block_size():
    # BlockSize 12800, 6400, 3200, 1600, 800
    assert BlockSize.from_int(12800) == BlockSize.BS_12800, "BlockSize enum error!"
    assert BlockSize.from_int(6400) == BlockSize.BS_6400, "BlockSize enum error!"
    assert BlockSize.from_int(3200) == BlockSize.BS_3200, "BlockSize enum error!"
    assert BlockSize.from_int(1600) == BlockSize.BS_1600, "BlockSize enum error!"
    assert BlockSize.from_int(800) == BlockSize.BS_800, "BlockSize enum error!"


def test_sample_rate():
    # SampleRate 48000, 44100, 24000, 22050, 16000, 11025
    assert SampleRate.from_int(48000) == SampleRate.SR_48000, "SampleRate enum error!"
    assert SampleRate.from_int(44100) == SampleRate.SR_44100, "SampleRate enum error!"
    assert SampleRate.from_int(24000) == SampleRate.SR_24000, "SampleRate enum error!"
    assert SampleRate.from_int(22050) == SampleRate.SR_22050, "SampleRate enum error!"
    assert SampleRate.from_int(16000) == SampleRate.SR_16000, "SampleRate enum error!"
    assert SampleRate.from_int(11025) == SampleRate.SR_11025, "SampleRate enum error!"


def test_voise_channel():
    # VoiceChannel "stereo", "mono"
    assert VoiceChannel.from_string("stereo") == VoiceChannel.CHANNEL_STEREO, (
        "VoiceChannel enum error!"
    )
    assert VoiceChannel.from_string("mono") == VoiceChannel.CHANNEL_MONO, (
        "VoiceChannel enum error!"
    )
