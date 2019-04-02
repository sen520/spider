# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from xiaoshuo_spider.items import XiaoshuoSpiderItem, BookSpiderItem


class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    allowed_domains = ['www.biquge5200.cc']

    # start_urls = ['https://www.biquge5200.cc/']

    # 获取初始url
    def start_requests(self):
        url = 'https://www.biquge5200.cc/'
        yield SplashRequest(url, callback=self.parse)

    # 解析初始页面
    def parse(self, response):
        # 分类名称
        type_list_name_get = response.xpath('//*[@id="wrapper"]/div[3]/ul/li/a/text()').extract()
        type_list_name = type_list_name_get[2:]
        # 分类链接
        type_list_url_get = response.xpath('//*[@id="wrapper"]/div[3]/ul/li/a/@href').extract()
        type_list_url = type_list_url_get[2:]

        for url in type_list_url:
            url = 'https:' + url
            yield SplashRequest(url, callback=self.parse_type)

    def parse_type(self, response):
        li = response.xpath('//*[@id="newscontent"]/div[1]/ul/li')
        # 获取分类
        type_get = li.xpath('//*[@id="newscontent"]/div[1]/h2/text()').extract_first()
        type = type_get[3:7]

        # 小说名列表
        book_names = li.xpath('./span[1]/a/text()').extract()

        # 作者名列表
        authors = li.xpath('./span[3]/text()').extract()

        # 最近更新章节
        latest_chapters = li.xpath('./span[2]/a/text()').extract()

        # 小说链接
        book_urls = li.xpath('./span[1]/a/@href').extract()

        for book_name, author, latest_chapter, book_url in zip(book_names, authors, latest_chapters, book_urls):
            item = XiaoshuoSpiderItem()
            item['type'] = type
            item['book_name'] = book_name
            item['author'] = author
            item['latest_chapter'] = latest_chapter
            item['book_url'] = book_url
            # print(item)
            yield item

            yield SplashRequest(item['book_url'], callback=self.parse_bookcontent)

    def parse_bookcontent(self, response):

        # 获取小说初始章节链接
        first_url = response.xpath('//*[@id="list"]/dl/dd[10]/a/@href').extract_first()
        yield SplashRequest(first_url, callback=self.parse_book)

    def parse_book(self, response):

        # 书名
        book_name = response.xpath('//*[@id="wrapper"]/div[4]/div/div[1]/a[3]/text()').extract_first()

        # 章节名
        chapter = response.xpath('//*[@id="wrapper"]/div[4]/div/div[2]/h1/text()').extract_first()

        # 内容
        content = response.xpath('string(//*[@id="content"])').extract_first()

        # 下一页地址
        next_page = response.xpath('//*[@id="wrapper"]/div[4]/div/div[8]/a[4]/@href').extract_first()

        item = BookSpiderItem()
        item['book_name'] = book_name
        item['chapter'] = chapter
        item['content'] = content
        yield item

        # 判断是否有下一页，如果有就继续执行
        if next_page:
            yield SplashRequest(next_page, callback=self.parse_book)
