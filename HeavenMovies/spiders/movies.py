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
        cleaned_lines = [re.sub(r'[\s\u3000\xa0]+', ' ', s).strip() for s in raw_lines if s.strip()]
        print("清洗后的数据:", cleaned_lines)

        parsed_data = self.parse_span_text_list(cleaned_lines)
        print("解析后字典:", parsed_data)

        item['title'] = parsed_data.get('译名', item['title'])
        item['year'] = self.extract_year(parsed_data.get('年代'))
        item['director'] = parsed_data.get('导演')
        item['actors'] = self.extract_list(parsed_data.get('主演'))
        item['description'] = parsed_data.get('简介')
        item['awards'] = self.extract_awards(parsed_data.get('获奖情况'))
        item['magnet_link'] = response.css('#Zoom a[href^="magnet:"]::attr(href)').get()

        yield item

    def parse_span_text_list(self, lines):
        result = {}
        current_key = None
        buffer = []

        for line in lines:
            # 先处理字段名，如：◎译 名 挚友/朋友
            match = re.match(r'^◎\s*([\u4e00-\u9fa5A-Za-z]+(?:\s*[\u4e00-\u9fa5A-Za-z]+)?)\s+(.*)', line)
            if match:
                # 保存前一个字段
                if current_key:
                    result[current_key] = '\n'.join(buffer).strip()
                    buffer = []

                # 处理新字段
                key = match.group(1).replace(' ', '')  # 移除字段名中的空格，如“译 名”→“译名”
                value = match.group(2).strip()
                current_key = key
                if value:
                    buffer.append(value)
            else:
                if current_key:
                    buffer.append(line.strip())

        # 处理最后一个字段
        if current_key and buffer:
            result[current_key] = '\n'.join(buffer).strip()

        return result

    def extract_year(self, text):
        if not text:
            return None
        match = re.search(r'\d{4}', text)
        return int(match.group()) if match else None

    def extract_list(self, text):
        if not text:
            return []
        return [line.strip() for line in text.split('\n') if line.strip()]

    def extract_awards(self, text):
        if not text:
            return []
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        result = []
        current_award = None
        for line in lines:
            if re.match(r'^第\d+届', line):
                current_award = {'event': line, 'items': []}
                result.append(current_award)
            elif current_award:
                current_award['items'].append(line)
        return result
