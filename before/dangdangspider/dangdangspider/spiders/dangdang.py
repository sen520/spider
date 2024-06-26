# -*- coding: utf-8 -*-
import random
import time
import scrapy
import scrapy_splash

from ..items import DangdangspiderItem


class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://search.dangdang.com/?key=python&act=input&page_index={}'.format(i) for i in range(1, 3)]

    def parse(self, response):
        url_list = response.xpath("//p[@name='title']/a/@href").extract()
        for url in url_list:
            yield scrapy_splash.SplashRequest(url, callback=self.parse_info)

    def parse_info(self, response):
        # 书名
        book_name = response.xpath("string(//h1/@title)").extract_first()

        # 简介
        simp_intro = response.xpath("//span[@class='head_title_name']/text()").extract_first()

        # 图片地址
        img_url = response.xpath("//a[@class='img']/img/@src").extract_first()

        # 作者
        author_list = response.xpath("//a[@dd_name='作者']/text()").extract()
        author = "".join(author_list)

        # 出版社
        publish = response.xpath("//a[@dd_name='出版社']/text()").extract_first()

        # 价格
        prices = response.xpath("string(//p[@id='dd-price'])").extract_first()
        price = prices.strip()

        # 书本详情
        details = response.xpath("string(//div[@class='pro_content']/ul)").extract_first()

        # 内容简介
        content = response.xpath("string(//div[@id='content']//div[@class='descrip'])").extract_first()
        if content == '':
            content = '没有查询到该数据'
        # 目录
        contents_str = response.xpath("string(//div[@id='catalog']/div[@class='descrip'])").extract_first()
        contents = contents_str.replace('<br />', '\n')
        if contents == '':
            contents = '没有查询到该数据'
        item = DangdangspiderItem()

        # 书名
        item['book_name'] = book_name

        # 简介
        item['simp_intro'] = simp_intro

        # 图片地址
        item['img_url'] = img_url

        # 图片名称
        item['img_name'] = str(img_url)[-18:]

        # 图片存储地址
        item['img_path'] = 'E:\Python\exe\\02spider\dangdangspider\dangdangspider\img\\' + item['img_name']

        # 作者
        item['author'] = author

        # 出版社
        item['publish'] = publish

        # 价格
        item['price'] = price

        # 书本详情
        item['details'] = details.strip()

        # 内容简介
        item['content'] = content

        # 目录
        item['contents'] = contents

        yield item
