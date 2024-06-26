# -*- coding: utf-8 -*-
import scrapy
from scrapy_spider_list.items import CityWeather
import re


class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['tianqi.com']
    # start_urls = ['http://lishi.tianqi.com/']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "cityPy=hefei; cityPy_expire=1565169169; UM_distinctid=16c474dd264a1-0b04273e7d2d77-3a65460c-1fa400-16c474dd26511b; Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1564564379; CNZZDATA1275796416=1009663516-1564561302-https%253A%252F%252Fwww.tianqi.com%252F%7C1564560013; Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2=1564565427",
            "Host": "lishi.tianqi.com",
            "Pragma": "no-cache",
            "Referer": "http://lishi.tianqi.com/chongqing/index.html",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        }
    }

    def start_requests(self):
        url = 'http://lishi.tianqi.com/'
        yield scrapy.Request(url, callback=self.get_city)

    def get_city(self, response):
        city_ele = response.xpath('//ul[@class="bcity"]/li/a[contains(@href, "http")]')
        for city in city_ele:
            city_href = city.xpath('./@href').extract_first()
            yield scrapy.Request(url=city_href, callback=self.city_parse)

    def city_parse(self, response):
        dates = response.xpath('//div[@class="tqtongji1"]//li/a')
        for date in dates:
            url = date.xpath('./@href').extract_first()
            yield scrapy.Request(url=url, callback=self.date_parse)

    def date_parse(self, response):
        uls = response.xpath('//div[@class="tqtongji2"]//ul')
        city_str = response.xpath('//div[@class="box-hd"]/h3/text()').extract_first()
        keys = ['city_name', 'date', 'ht', 'lt', 'weather', 'wind_dir']
        for ul in uls:
            city = CityWeather()
            datas = [re.search('(\w+)\d{4}', city_str)[1]]
            li = ul.xpath('./li//text()').extract()
            if li[0] == '日期':
                continue
            else:
                datas += li
            for value, key in zip(datas, keys):
                city[key] = value
            yield city
