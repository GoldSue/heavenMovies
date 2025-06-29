# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HeavenmoviesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    year_of_release = scrapy.Field()
    type_of_movie = scrapy.Field()
    location = scrapy.Field()
    imdb_score = scrapy.Field()
    douban_score = scrapy.Field()
    duration = scrapy.Field()
    language = scrapy.Field()
    intro = scrapy.Field()
    # award_number = scrapy.Field()
    # award_name = scrapy.Field()
    magnet_link = scrapy.Field()

