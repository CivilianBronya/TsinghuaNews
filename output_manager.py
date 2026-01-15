from pathlib import Path
from datetime import datetime
import pandas as pd


class OutputManager:
    def __init__(self, project_name="TsinghuaNews"):
        self.project_name = project_name
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.list_pages_file = self.output_dir / f"{project_name}_list_pages_{timestamp}.xlsx"
        self.news_links_file = self.output_dir / f"{project_name}_news_links_{timestamp}.xlsx"

        self.list_pages_data = []  # 每页 URL
        self.news_links_data = []  # 每条新闻数据

    def write_list_page(self, page_index: int, url: str):
        # 记录列表页 URL
        self.list_pages_data.append({
            "page_index": int(page_index),
            "url": str(url)
        })

    def write_news_links(self, news_list: list):
        # 记录所有新闻链接，确保字符串格式
        for news in news_list:
            self.news_links_data.append({
                "title": str(news.get("title", "")),
                "url": str(news.get("url", "")),
                "date": str(news.get("date", "")),
                "source_page": str(news.get("source_page", ""))
            })

    def save_all(self):
        if self.list_pages_data:
            df_pages = pd.DataFrame(self.list_pages_data)
            df_pages.to_excel(self.list_pages_file, index=False, engine="openpyxl")

        if self.news_links_data:
            df_news = pd.DataFrame(self.news_links_data)
            df_news.to_excel(self.news_links_file, index=False, engine="openpyxl")

    def get_list_pages_path(self):
        return str(self.list_pages_file)

    def get_news_links_path(self):
        return str(self.news_links_file)
