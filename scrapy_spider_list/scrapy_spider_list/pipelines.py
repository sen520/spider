# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy_spider_list.settings import mongo
from pymongo import MongoClient
from scrapy_spider_list.items import CityWeather, Book


class SpiderPipeline(object):

    # start MongoDB client
    def open_spider(self, spider):
        self.client = MongoClient(
            host=mongo["MONGODB_HOST"],
            # port=mongo['MONGODB_PORT'],
        )
        self.db = self.client[mongo['MONGODB_DBNAME']]

    # insert data
    def process_item(self, item, spider):
        # Determine the value passed from which item
        if isinstance(item, CityWeather):
            if self.db.weather.find_one({'city': item['city'], 'date': item['date']}):
                pass
            else:
                self.db.weather.insert(item)
        elif isinstance(item, Book):
            if self.db.book.find_one({'book_name': item['book_name'], 'chapter_name': item['chapter_name']}):
                pass
            else:
                self.db.book.insert(item)
        return item

    # close client
    def close_spider(self, spider):
        self.client.close()
