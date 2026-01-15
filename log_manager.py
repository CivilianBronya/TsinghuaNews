# log_manager.py
import logging
from pathlib import Path
from datetime import datetime

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

_logger = None


def get_logger(project_name: str = "TsinghuaNews"):
    """
    获取全局唯一 logger（只初始化一次）
    """
    global _logger

    if _logger:
        return _logger

    logger = logging.getLogger(project_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        _logger = logger
        return logger

    log_file = LOG_DIR / f"{project_name}_{datetime.now():%Y%m%d_%H%M%S}.log"

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    _logger = logger
    return logger


# 下面全是「纯日志函数」

def log_start(project, crawl, debug):
    logger = get_logger(project.get("name"))
    logger.info("========== 爬虫任务启动 ==========")
    logger.info("项目：%s", project.get("name"))
    logger.info("目标：%s", project.get("target"))
    logger.info("起始页：%s", crawl.get("start_url"))
    logger.info("Debug：%s", debug.get("enable"))
    logger.info("\n")


def log_page_crawl(page_index, new_count, debug=False, max_pages=None):
    logger = get_logger()
    logger.info("第 %d 页完成，新增 %d 条新闻", page_index, new_count)

    if debug and max_pages and page_index >= max_pages:
        logger.warning("DEBUG 模式生效，达到最大页数，提前停止")


def log_finish(pages, total, list_file=None, news_file=None):
    logger = get_logger()
    logger.info("========== 爬虫任务完成 ==========")
    logger.info("页数：%d", pages)
    logger.info("新闻数：%d", total)

    if list_file:
        logger.info("列表页文件：%s", list_file)
    if news_file:
        logger.info("新闻链接文件：%s", news_file)
