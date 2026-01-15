from config.settings import CRAWL, DEBUG
from log_manager import get_logger
import requests, time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

logger = get_logger("TsinghuaNews")


BASE = CRAWL["base_url"]
START = CRAWL["start_url"]
TIMEOUT = CRAWL["timeout_seconds"]
SLEEP = CRAWL["sleep_seconds"]

session = requests.Session()
session.headers = {"User-Agent": "Mozilla/5.0"}

import re
# http://www.tsinghua.edu.cn/info/xxxx/yyyyyy.htm
NEWS_DETAIL_PATTERN = re.compile(r"/info/\d+/\d+\.htm$")

def is_news_detail_url(url: str) -> bool:
    return bool(NEWS_DETAIL_PATTERN.search(url))


def parse_list_page(url):
    resp = session.get(url, timeout=TIMEOUT)
    resp.raise_for_status()

    # 编码兜底（这是正确写法）
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, "html.parser")

    news_list = []

    for li in soup.select("ul li"):
        a = li.find("a")
        if not a:
            continue

        href = a.get("href")
        if not href:
            continue

        link = urljoin(BASE, href)

        # 保留单条新闻详情页
        if not is_news_detail_url(link):
            continue

        title = a.get_text(strip=True)
        date = li.find("span").get_text(strip=True) if li.find("span") else None

        news_list.append({
            "title": title,
            "url": link,
            "date": date,
            "source_page": url
        })
    # print(news_list)
    # 下一页逻辑
    page_div = soup.find("div", class_="pb_sys_common")
    if page_div:
        next_span = page_div.find("span", class_="p_next")
        if next_span:
            next_a = next_span.find("a")
            if next_a:
                next_url = urljoin(url, next_a.get("href"))
                return news_list, next_url

    return news_list, None



def fetch_news_list():
    """
    负责爬取新闻列表，返回数据给 OutputManager 或其他处理函数
    """
    visited_pages = set()
    all_news = []

    url = START
    page_index = 1

    while url and url not in visited_pages:
        visited_pages.add(url)

        try:
            page_news, next_url = parse_list_page(url)
        except Exception as e:
            # 可以交给 log_manager 统一记录
            from log_manager import log_page_error
            log_page_error(page_index, str(e))
            break

        all_news.extend(page_news)

        # 日志封装输出（统一调用 log_manager）
        from log_manager import log_page_crawl

        log_page_crawl(
            page_index,
            len(page_news),
            debug=DEBUG["enable"],
            max_pages=DEBUG.get("max_pages")
        )

        if DEBUG["enable"] and page_index >= DEBUG["max_pages"]:
            break

        url = next_url
        page_index += 1
        time.sleep(SLEEP)

    return {
        "pages": page_index,
        "news_count": len(all_news),
        "total": len(all_news),
        "news": all_news,
        "visited_pages": visited_pages
    }

