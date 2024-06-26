# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_spider_list.items import Book
from scrapy_redis.spiders import RedisSpider


class BiqugeSpider(RedisSpider):
    name = 'biqugeDistributed'
    allowed_domains = ['biqugex.com']
    redis_key = 'biquge:start_urls'

    def parse(self, response):
        links = LinkExtractor(restrict_xpaths='//a[contains(@href,"/book_")]')
        for link in links.extract_links(response):
            yield scrapy.Request(url=link.url, dont_filter=False, callback=self.chapter)

    def chapter(self, response):
        chapter_links = LinkExtractor(restrict_xpaths='//a[contains(@href,"/book_")]', deny='book_.*/$')
        for chapter_link in chapter_links.extract_links(response):
            yield scrapy.Request(url=chapter_link.url, dont_filter=False, callback=self.content)

    def content(self, response):
        book = Book()
        book['book_name'] = response.xpath('//div[@class="path"]/div[@class="p"]/a[2]/text()').extract_first()
        book['chapter_name'] = response.xpath('//h1/text()').extract_first()
        content_list = response.xpath('//div[@id="content"]/text()').extract()
        book['content'] = '\n'.join(map(
            lambda line: line.strip(), content_list))
        yield book
