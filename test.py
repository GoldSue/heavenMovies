import re

import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from HeavenMovies.items import HeavenmoviesItem


class MoviesSpider(scrapy.Spider):
    name = "movies"
    allowed_domains = ["dytt8.com"]
    start_urls = ["https://www.dytt8.com/"]

    def parse(self, response):
        # 所有电影链接（通常是 a 标签）
        for a in response.css('div.co_content2 ul a'):
            raw_title = a.css('::text').get()
            raw_url = a.css('::attr(href)').get()
            detail_url = response.urljoin(raw_url)

            print('原始数据:', raw_title,"数据连接：", detail_url)

            # 校验数据
            if not detail_url or not raw_title:
                continue

            # 提取《xxx》格式的电影标题
            match = re.search(r'《(.*?)》', raw_title)
            title = match.group(1) if match else raw_title.strip()

            # 构造 item
            movie_item = HeavenmoviesItem()
            movie_item['title'] = title

            # 补全为绝对路径
            full_url = response.urljoin(detail_url)

            yield Request(
                url=full_url,
                callback=self.parse_detail,
                cb_kwargs={'item': movie_item},
            )

    def parse_span_text_list(info_list):
        result = {}
        current_key = None
        buffer = []

        for line in info_list:
            # 清洗：去掉 ◎、中文空格、不间断空格、去除两端空白
            line = line.replace('\xa0', ' ')
            line = re.sub(r'[◎\u3000]+', '', line).strip()

            # 跳过空行
            if not line:
                continue

            # 匹配字段名，如：IMDb评分: 5.6/10
            match = re.match(r'^(.+?[：:])\s*(.*)', line)
            if match:
                # 如果上一个字段有内容累积，先保存
                if current_key and buffer:
                    result[current_key] = '\n'.join(buffer).strip()
                    buffer = []

                current_key = match.group(1).strip()
                value = match.group(2).strip()

                if value:
                    result[current_key] = value
                    current_key = None  # 如果本行已经有值，就不用缓存后续行
            else:
                # 多行内容拼接
                if current_key:
                    buffer.append(line)

        # 最后处理未保存的字段
        if current_key and buffer:
            result[current_key] = '\n'.join(buffer).strip()

        return result

    def parse_detail(self, response: HtmlResponse, item: HeavenmoviesItem):
        info_list = response.css('#Zoom ::text').getall()
        print('详情数据:', info_list)
        # 步骤1 & 2: 预处理和清洗字符串
        cleaned_info = []
        for s in info_list:
            # 替换各种空白字符为标准空格，并处理多余空格，然后去除首尾空格
            s = re.sub(r'[\s\u3000\xa0]+', ' ', s).strip()
            if s:  # 只保留非空字符串
                cleaned_info.append(s)

        print('清洗后的数据:', cleaned_info)

        # 步骤3: 针对性解析
        description_started = False
        actors_list = []

        for line in cleaned_info:
            if line.startswith('◎译 名'):
                item.title = line.replace('◎译 名 ', '').strip()
            elif line.startswith('◎片 名'):
                # 假设你可能需要片名，这里可以赋值给另一个字段或者进一步处理
                pass
            elif line.startswith('◎年 代'):
                try:
                    item.year = int(line.replace('◎年 代 ', '').strip())
                except ValueError:
                    item.year = None  # 或者记录错误
            elif line.startswith('◎导 演'):
                item.director = line.replace('◎导 演 ', '').strip()
            elif line.startswith('◎主 演'):
                # 第一个主演会在这一行，后面的主演在后续行
                actors_list.append(line.replace('◎主 演 ', '').strip())
            elif description_started:
                # 已经开始解析简介了，继续追加
                if item.description:
                    item.description += "\n" + line
                else:
                    item.description = line
            elif line.startswith('◎简 介'):
                description_started = True
                # 简介可能在同一行，也可能在下一行，这里只标记开始
            elif actors_list and not line.startswith('◎'):
                # 如果已经开始收集主演，且当前行不是新的◎开头的字段，则认为是主演的延续
                actors_list.append(line)
            # 你可以根据需要添加更多条件来解析其他字段

        item.actors = [actor for actor in actors_list if actor]  # 确保演员列表中没有空字符串

        # 最后，处理简介，通常简介会是多行文本，需要合并
        # 注意：这里的简介处理比较简化，如果简介内容可能包含其他信息，需要更复杂的逻辑
        # item.description 在循环中已经处理过了，这里只是一个提醒，确认是否需要额外的后处理

        print(f"提取的标题: {item.title}")
        print(f"提取的年份: {item.year}")
        print(f"提取的导演: {item.director}")
        print(f"提取的演员: {item.actors}")
        print(f"提取的简介: {item.description}")

        # item['year_of_release'] = info_dict.get('年代:')
        # item['type_of_movie'] = info_dict.get('类型:')
        # item['location'] = info_dict.get('产地:')
        # item['imdb_score'] = info_dict.get('IMDb评分:')
        # item['douban_score'] = info_dict.get('豆瓣评分:')
        # item['duration'] = info_dict.get('片长:')
        # item['language'] = info_dict.get('语言:')
        # item['intro'] = info_dict.get('简介:')
        item['magnet_link'] = response.css('#Zoom a[href^="magnet:"]::attr(href)').get()

        yield item

