# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from xiaoshuo_spider.settings import MYSQL
from xiaoshuo_spider.items import XiaoshuoSpiderItem, BookSpiderItem


class XiaoshuoMySQLSpiderPipeline(object):

    # 开启MySQL数据库链接
    def open_spider(self, spider):
        self.connection = pymysql.connect(MYSQL["host"], MYSQL["user"], MYSQL["password"], MYSQL["db"], MYSQL["port"],
                                          charset="utf8")

        self.cursor = self.connection.cursor()

    # 插入数据
    def process_item(self, item, spider):
        # 判断是从那个item传过来的值
        if isinstance(item, XiaoshuoSpiderItem):
            sql = 'insert into t_biquge VALUES (0,%s,%s,%s,%s)'
            self.cursor.execute(sql,
                                [item['type'], item['book_name'], item['author'], item['latest_chapter']])
            self.connection.commit()
        return item

    # 关闭连接
    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()


class XiaoshuoFileSpiderPipeline(object):
    def open_spider(self, spider):
        pass

    # 写入文件
    def process_item(self, item, spider):
        # 判断是从那个item传过来的值
        if isinstance(item, BookSpiderItem):
            with open("./static/" + item["book_name"] + ".txt", 'a', encoding="utf-8") as file:
                file.write(item["chapter"])
                file.write(item["content"])

        return item

    def close_spider(self, spider):
        pass
