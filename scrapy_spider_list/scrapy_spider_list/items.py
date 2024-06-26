# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CityWeather(scrapy.Item):
    _id = scrapy.Field()
    city = scrapy.Field()
    date = scrapy.Field()
    ht = scrapy.Field()
    lt = scrapy.Field()
    weather = scrapy.Field()
    wind_dir = scrapy.Field()


class Book(scrapy.Item):
    _id = scrapy.Field()
    book_name = scrapy.Field()
    chapter_name = scrapy.Field()
    content = scrapy.Field()
