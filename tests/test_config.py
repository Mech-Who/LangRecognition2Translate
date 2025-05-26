# 暂时只能通过sys.path完成，没找到其他方案
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

# third-party
import pytest

# custom
from src.utils.config import config


@pytest.mark.parametrize("config_key", ["general", "recognition", "translation"])
def test_config(config_key: str):
    assert config[config_key] is not None, "Config lost key!"
