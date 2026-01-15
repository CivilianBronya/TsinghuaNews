# news_detail.py
import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from log_manager import get_logger

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

logger = get_logger()


def fetch_news_detail(url, save_root="output/news"):
    """
    抓取单条新闻详情（文本 + 图片）
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
    except Exception as e:
        logger.error("请求失败: %s | %s", url, e)
        return False

    soup = BeautifulSoup(resp.text, "html.parser")

    news_id = url.rstrip(".htm").split("/")[-1]
    news_dir = os.path.join(save_root, news_id)
    img_dir = os.path.join(news_dir, "images")

    os.makedirs(img_dir, exist_ok=True)

    # 标题
    title_tag = soup.select_one("div.nry_bt_real p.bt")
    title = title_tag.get_text(strip=True) if title_tag else "无标题"

    # 正文
    content_div = soup.find("div", class_="v_news_content")
    paragraphs = []

    if content_div:
        for p in content_div.find_all("p"):
            text = p.get_text(strip=True)
            if text:
                paragraphs.append(text)

    # 保存文本
    with open(os.path.join(news_dir, "content.txt"), "w", encoding="utf-8") as f:
        f.write(title + "\n\n")
        f.write("\n".join(paragraphs))

    # 图片
    if content_div:
        for idx, img in enumerate(content_div.find_all("img"), 1):
            src = img.get("src")
            if not src:
                continue

            img_url = urljoin(url, src)
            ext = os.path.splitext(urlparse(img_url).path)[1] or ".jpg"
            img_path = os.path.join(img_dir, f"img_{idx}{ext}")

            _download_image(img_url, img_path)

    logger.info("新闻保存完成: %s", news_id)
    return True


def _download_image(url, save_path):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r.content)
    except Exception as e:
        logger.warning("图片下载失败: %s | %s", url, e)


def process_news_list(news_list, limit=100):
    """
    批量处理新闻详情
    """
    total = min(len(news_list), limit)
    success = 0
    failed = 0

    logger.info("开始抓取新闻详情：共 %d 条", total)

    for idx, item in enumerate(news_list[:total], 1):
        url = item.get("url")
        if not url:
            failed += 1
            continue

        logger.info("抓取中 [%d/%d]", idx, total)

        if fetch_news_detail(url):
            success += 1
        else:
            failed += 1

    logger.info(
        "新闻详情抓取完成：成功 %d，失败 %d",
        success,
        failed
    )

    return {
        "success": success,
        "failed": failed
    }
