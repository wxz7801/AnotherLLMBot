import os
import tomllib


def read_config(t_path: str = "config.toml"):
    if os.path.exists(t_path):
        # 读取并解析 TOML 文件（必须用二进制模式打开！）
        with open("config.toml", "rb") as f:  # 注意 "rb" 模式
            return tomllib.load(f)
    else:
        raise FileNotFoundError(f"配置文件 {t_path} 不存在！")

config = read_config("./config.toml")