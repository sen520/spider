# -*- coding: utf-8 -*-
import scrapy

class DownloadImageSpider(scrapy.Spider):
    name = 'download_image'
    allowed_domains = ['image.baidu.com']
    start_urls = [
        'http://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gb18030&word=%CD%BC%C6%AC&fr=ala&ala=1&alatpl=others&pos=0']

    def parse(self, response):
        links = response.xpath('//img/@src').extract()
        url_list = []
        for link in links:
            url = response.urljoin(link)
            url_list.append(url)
        yield {'image_urls': url_list}
