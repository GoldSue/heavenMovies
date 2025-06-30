# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


import scrapy


class HeavenmoviesItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()
    director = scrapy.Field()
    actors = scrapy.Field()
    language = scrapy.Field()
    genre = scrapy.Field()
    duration = scrapy.Field()
    imdb_score = scrapy.Field()
    douban_score = scrapy.Field()
    description = scrapy.Field()
    awards = scrapy.Field()
    magnet_link = scrapy.Field()


    # title = scrapy.Field()
    # year_of_release = scrapy.Field()
    # type_of_movie = scrapy.Field()
    # location = scrapy.Field()
    # imdb_score = scrapy.Field()
    # douban_score = scrapy.Field()
    # duration = scrapy.Field()
    # language = scrapy.Field()
    # intro = scrapy.Field()
    # magnet_link = scrapy.Field()

    # award_number = scrapy.Field()
    # award_name = scrapy.Field()


