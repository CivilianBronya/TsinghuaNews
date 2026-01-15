from pathlib import Path
import jieba
from collections import Counter
from log_manager import get_logger

NEWS_ROOT = Path("output/news")
TOP_N = 10

logger = get_logger("word_analyzer")


def load_all_news_text(news_root: Path) -> str:
    """
    读取所有新闻 content.txt，合并成一个大文本
    """
    texts = []
    count = 0

    for news_dir in news_root.iterdir():
        if not news_dir.is_dir():
            continue

        content_file = news_dir / "content.txt"
        if not content_file.exists():
            continue

        text = content_file.read_text(encoding="utf-8").strip()
        if text:
            texts.append(text)
            count += 1

    logger.info("成功读取 %d 篇新闻正文", count)
    return "\n".join(texts)


def analyze_top_words(text: str, top_n: int = 10):
    """
    分词并统计词频
    """
    if not text.strip():
        logger.warning("文本为空，跳过分词统计")
        return []

    words = jieba.lcut(text)

    # 基础过滤：长度 + 空白
    words = [
        w for w in words
        if len(w) >= 2 and not w.isspace()
    ]

    logger.info("分词完成，词语数量：%d", len(words))

    counter = Counter(words)
    return counter.most_common(top_n)


def main():
    if not NEWS_ROOT.exists():
        logger.error("新闻目录不存在：%s", NEWS_ROOT)
        return

    logger.info("开始新闻文本分词分析")

    text = load_all_news_text(NEWS_ROOT)
    top_words = analyze_top_words(text, TOP_N)

    logger.info("出现次数最多的前 %d 个词语：", TOP_N)
    for word, count in top_words:
        logger.info("%s：%d", word, count)


if __name__ == "__main__":
    main()
