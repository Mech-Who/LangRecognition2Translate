# 暂时只能通过sys.path完成，没找到其他方案
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pytest

# custom
from src.utils.constants import (
    BlockSize,
    Format,
    Language,
    SampleRate,
    VoiceChannel,
)


@pytest.mark.parametrize(
    "lang_code, lang_enum",
    [
        ("zh", Language.CHINESE),
        ("en", Language.ENGLISH),
        ("jp", Language.JAPANESE),
        ("ko", Language.KOREAN),
    ],
)
def test_language(lang_code: str, lang_enum: Language):
    # Language "zh", "en", "jp", "ko"
    assert Language.from_string(lang_code) == lang_enum, "Language enum error!"


@pytest.mark.parametrize(
    "format_code, format_enum",
    [
        ("pcm", Format.F_PCM),
        ("wav", Format.F_WAV),
        ("opus", Format.F_OPUS),
        ("speex", Format.F_SPEEX),
        ("aac", Format.F_AAC),
        ("amr", Format.F_AMR),
    ],
)
def test_format(format_code: str, format_enum: Format):
    # Format "pcm", "wav", "opus", "speex", "aac", "amr"
    assert Format.from_string(format_code) == format_enum, "Format enum error!"


@pytest.mark.parametrize(
    "block_size_value, block_size_enum",
    [
        (12800, BlockSize.BS_12800),
        (6400, BlockSize.BS_6400),
        (3200, BlockSize.BS_3200),
        (1600, BlockSize.BS_1600),
        (800, BlockSize.BS_800),
    ],
)
def test_block_size(block_size_value: int, block_size_enum: BlockSize):
    # BlockSize 12800, 6400, 3200, 1600, 800
    assert BlockSize.from_int(block_size_value) == block_size_enum, (
        "BlockSize enum error!"
    )


@pytest.mark.parametrize(
    "sample_rate_value, sample_rate_enum",
    [
        (48000, SampleRate.SR_48000),
        (44100, SampleRate.SR_44100),
        (24000, SampleRate.SR_24000),
        (22050, SampleRate.SR_22050),
        (16000, SampleRate.SR_16000),
        (11025, SampleRate.SR_11025),
    ],
)
def test_sample_rate(sample_rate_value: int, sample_rate_enum: SampleRate):
    # SampleRate 48000, 44100, 24000, 22050, 16000, 11025
    assert SampleRate.from_int(sample_rate_value) == sample_rate_enum, (
        "SampleRate enum error!"
    )


@pytest.mark.parametrize(
    "channel_code, channel_enum",
    [("stereo", VoiceChannel.CHANNEL_STEREO), ("mono", VoiceChannel.CHANNEL_MONO)],
)
def test_voise_channel(channel_code: str, channel_enum: VoiceChannel):
    # VoiceChannel "stereo", "mono"
    assert VoiceChannel.from_string(channel_code) == channel_enum, (
        "VoiceChannel enum error!"
    )
