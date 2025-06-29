# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class HeavenmoviesPipeline:

    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',port=3306,
                                    user='root',password='Gold7789@',
                                    database='scrapy',charset='utf8mb4'
                                    )
        self.cursor = self.conn.cursor()
        self.data = []

    def close_spider(self, spider):
        if len(self.data) > 0:
            self.write_to_db()
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        title = item.get('title', '')
        year_of_release = item.get('year_of_release', '')
        type_of_movie = item.get('type_of_movie', '')
        location = item.get('location', '')
        imdb_score = item.get('imdb_score', '')
        douban_score = item.get('douban_score', '')
        duration = item.get('duration', '')
        language = item.get('language', '')
        intro = item.get('intro', '')
        rank = item.get('rank', '')
        magnet_link = item.get('magnet_link', '')
        self.data.append((title, year_of_release, type_of_movie, location, imdb_score, douban_score, duration, language, intro, rank, magnet_link))
        if len(self.data) > 100:
            self.write_to_db()
            self.conn.commit()
            self.data.clear()

        return item

    def write_to_db(self):
        self.cursor.executemany(
            '''
            INSERT INTO heaven_movie (
                title, year, type, location,
                imdb_score, douban_score, duration,
                language, intro
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''',
            self.data
        )