from request import fetch_news_list
from output_manager import OutputManager
from news_detail import process_news_list
from log_manager import log_start, log_finish, get_logger
from config.settings import PROJECT, CRAWL, DEBUG


def main():
    # 初始化 logger（只做一次）
    get_logger(PROJECT.get("name"))

    # 启动日志
    log_start(PROJECT, CRAWL, DEBUG)

    # 抓列表页
    result = fetch_news_list()
    news_list = result["news"]

    # 输出 Excel
    output = OutputManager(PROJECT.get("name"))

    for idx, url in enumerate(result["visited_pages"], 1):
        output.write_list_page(idx, url)

    output.write_news_links(news_list)
    output.save_all()

    # 抓详情页（100 条）
    process_news_list(news_list, limit=100)

    # 完成日志
    log_finish(
        result["pages"],
        result["total"],
        output.get_list_pages_path(),
        output.get_news_links_path()
    )


if __name__ == "__main__":
    main()
