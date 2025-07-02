import re
import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse
from HeavenMovies.items import HeavenmoviesItem


class MoviesSpider(scrapy.Spider):
    name = "movies"
    allowed_domains = ["dytt8.com"]
    start_urls = ["https://www.dytt8.com/"]

    def parse(self, response):
        for a in response.css('div.co_content2 ul a'):
            raw_title = a.css('::text').get()
            raw_url = a.css('::attr(href)').get()
            detail_url = response.urljoin(raw_url)

            if not detail_url or not raw_title:
                continue

            match = re.search(r'《(.*?)》', raw_title)
            title = match.group(1) if match else raw_title.strip()

            movie_item = HeavenmoviesItem()
            movie_item['title'] = title

            yield Request(
                url=detail_url,
                callback=self.parse_detail,
                cb_kwargs={'item': movie_item},
            )

    def parse_detail(self, response: HtmlResponse, item: HeavenmoviesItem):
        raw_lines = response.css('#Zoom ::text').getall()
        cleaned_lines = [re.sub(r'[\s\u3000\xa0\'◎]+', ' ', s).strip() for s in raw_lines if s.strip()]
        # print("清洗后的数据:", cleaned_lines)

        parsed_data = self.parse_span_text_list(cleaned_lines)
        # print("解析后字典:", parsed_data)

        item['title'] = parsed_data.get('title', None)
        item['year'] = parsed_data.get('year', None)
        item['region'] = parsed_data.get('region', None)
        item['language'] = parsed_data.get('language', None)
        item['genre'] = parsed_data.get('genre', None)
        item['duration'] = parsed_data.get('duration', None)
        item['imdb'] = parsed_data.get('imdb', None)
        item['douban'] = parsed_data.get('douban', None)
        item['description'] = parsed_data.get('description', None)
        item['awards'] = parsed_data.get('awards', None)
        item['magnet_link'] = response.css('#Zoom a[href^="magnet:"]::attr(href)').get()

        yield item

    def parse_span_text_list(self, lines):
        result = {}
        n = len(lines)

        for i, line in enumerate(lines):
            # 提取 title（从带有 .2024. 的文件名中提取）
            match = re.match(r'^(.*?)\.\d{4}\.', line)
            if match:
                result["title"] = match.group(1).strip()
            elif line.startswith("年 代"):
                m = re.search(r'(\d{4})', line)
                if m:
                    result["year"] = m.group(1)
            elif line.startswith("语 言"):
                result["language"] = line.replace("语 言", "").strip()
            elif line.startswith("产 地"):
                result["region"] = line.replace("产 地", "").strip()
            elif line.startswith("类 别"):
                result["genre"] = line.replace("类 别", "").strip()
            elif "IMDb评分" in line:
                m = re.search(r'IMDb评分\s*([\d.]+)', line)
                if m:
                    result["imdb"] = m.group(1)
            elif "豆瓣评分" in line:
                m = re.search(r'豆瓣评分\s*([\d.]+)', line)
                if m:
                    result["douban"] = m.group(1)
            elif line.startswith("片 长"):
                m = re.search(r'(\d+)\s*分钟', line)
                if m:
                    result["duration"] = m.group(1)
            elif line.strip() == "简 介" and i + 1 < n:
                result["description"] = lines[i + 1].strip()
            elif line.strip() == "获奖情况":
                result["awards"] = lines[i + 1: -1]  # 倒数第1是视频文件名，跳过

        return result




