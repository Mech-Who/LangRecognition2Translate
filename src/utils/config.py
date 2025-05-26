# standard
from tomlkit import dump, load


def save_config(config, cfg_path: str = None):
    save_path = cfg_path if cfg_path else cfg_path
    with open(save_path, "w") as f:
        dump(config, f)


def load_config(cfg_path: str):
    with open(cfg_path, "r") as f:
        config = load(f)
    return config


# FIX: 路径配置是绝对路径，需要改成相对路径
config = load_config(r"C:\UserData\Projects\GithubTool\KoreanRecognition\config.toml")


if __name__ == "__main__":
    ...
