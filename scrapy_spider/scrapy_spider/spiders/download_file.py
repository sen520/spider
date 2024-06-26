# -*- coding: utf-8 -*-
import scrapy
from scrapy_spider.items import FileDownItem
from scrapy.linkextractors import LinkExtractor

class DownloadSpider(scrapy.Spider):
    name = 'download_file'
    allowed_domains = ['matplotlib.org']
    start_urls = ['https://matplotlib.org/examples/index.html']

    def parse(self, response):
        le = LinkExtractor(restrict_css='div.toctree-wrapper.compound',deny='/index.html$')
        print(len(le.extract_links(response)))
        for link in le.extract_links(response):
            yield scrapy.Request(url=link.url, callback=self.parse_result)

    def parse_result(self, response):
        hrefs = response.css('a.reference.external::attr(href)').extract()
        url_list = []
        for href in hrefs:
            url = response.urljoin(href)
            url_list.append(url)

        file = FileDownItem()
        file['file_urls'] = url_list
        return file