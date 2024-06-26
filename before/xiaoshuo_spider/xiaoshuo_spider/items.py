# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoshuoSpiderItem(scrapy.Item):
    # define the fields for your item here like:

    # 类型
    type = scrapy.Field()

    # 书名
    book_name = scrapy.Field()

    # 作者
    author = scrapy.Field()

    # 最新章节
    latest_chapter = scrapy.Field()

    # 小说url地址
    book_url = scrapy.Field()


class BookSpiderItem(scrapy.Item):
    # define the fields for your item here like:

    # 书名
    book_name = scrapy.Field()

    # 章节
    chapter = scrapy.Field()

    # 内容
    content = scrapy.Field()
