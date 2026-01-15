import json
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 配置文件路径
CONFIG_PATH = BASE_DIR / "config" / "crawl_config.json"
# print(CONFIG_PATH)
# 读取配置
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    _config = json.load(f)

# 对外暴露的配置

PROJECT = _config["project"]
CRAWL = _config["crawl"]
RETRY = _config["retry"]
DEBUG = _config["debug"]

# python打印
# print(PROJECT,CRAWL,RETRY,DEBUG)