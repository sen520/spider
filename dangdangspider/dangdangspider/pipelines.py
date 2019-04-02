# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class MongodbPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.dangdang = self.client.dangdang
        self.book = self.dangdang.book

    def process_item(self, item, spider):
        self.book.insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()


class MysqlPipeline(object):
    def open_spider(self, spider):
        self.client = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="spider",
                                      charset="utf8")
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        sql = 'insert into t_dangdang VALUES (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(sql,
                            [item['book_name'], item['simp_intro'], item['img_url'], item['img_path'], item['img_name'],
                             item['author'], item['publish'], item['price'], item['details'], item['content'],
                             item['contents']])
        self.client.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.client.close()


class ImgeDownLoadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item["img_url"], meta={"item": item})

    def file_path(self, request, response=None, info=None):
        item = request.meta["item"]
        file_name = item["img_name"]
        return file_name
