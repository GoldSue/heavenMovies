# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql


class HeavenmoviesPipeline:
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user='root', password='Gold7789@',
            database='scrapy', charset='utf8mb4'
        )
        self.cursor = self.conn.cursor()
        self.data = []

    def close_spider(self, spider):
        if self.data:
            self.write_to_db()
            self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        title = item.get('title', '')
        year = item.get('year', '')
        genre = item.get('genre', '')
        region = item.get('region', '')
        imdb = self.try_float(item.get('imdb'))
        douban = self.try_float(item.get('douban'))
        duration = self.try_int(item.get('duration'))
        language = item.get('language', '')
        description = item.get('description', '')
        rank = item.get('rank', '')
        magnet_link = item.get('magnet_link', '')

        self.data.append((
            title, year, genre, region,
            imdb, douban, duration, language,
            description, rank, magnet_link
        ))

        # 插入数据每2条写一次（可调节）
        if len(self.data) >= 2:
            self.write_to_db()
            self.conn.commit()
            self.data.clear()

        return item

    def write_to_db(self):
        sql = '''
            INSERT IGNORE INTO heaven_movie (
                title, year, genre, region,
                imdb_score, douban_score, duration,
                language, intro, `rank`, magnet_link
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        for row in self.data:
            try:
                self.cursor.execute(sql, row)
            except Exception as e:
                print(f'[写入失败] {e} -> {row}')

    def try_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def try_int(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
