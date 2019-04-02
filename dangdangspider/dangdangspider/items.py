# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DangdangspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 书名
    book_name = scrapy.Field()

    # 简介
    simp_intro = scrapy.Field()

    # 图片地址
    img_url = scrapy.Field()

    # 图片保存地址
    img_path = scrapy.Field()

    # 图片名称
    img_name = scrapy.Field()

    # 作者
    author = scrapy.Field()

    # 出版社
    publish = scrapy.Field()

    # 价格
    price = scrapy.Field()

    # 书本详情
    details = scrapy.Field()

    # 内容简介
    content = scrapy.Field()

    # 目录
    contents = scrapy.Field()
