# -*- coding: utf-8 -*-
import scrapy
import re
from pymongo import MongoClient
from scrapy_spider_list.items import CityWeather
from scrapy_spider_list.settings import mongo
from datetime import datetime

class NewweatherspiderSpider(scrapy.Spider):
    name = 'newWeatherSpider'
    allowed_domains = ['tianqi.com']
    start_urls = ['http://tianqi.com/']
    base_url = 'http://lishi.tianqi.com/'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "UM_distinctid=16ed50f775e205-069c9e121647e2-514f291a-1fa400-16ed50f775f3cc; cityPy=hefei; cityPy_expire=1576143535; CNZZDATA1275796416=1142425679-1575534457-%7C1575595001; Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1575536412,1575596606; Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2=1575596606",
            "Host": "lishi.tianqi.com",
            "Pragma": "no-cache",
            "Referer": "http://lishi.tianqi.com/chongqing/index.html",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        }
    }
    client = MongoClient(
        host=mongo["MONGODB_HOST"],
        # port=mongo['MONGODB_PORT'],
    )
    db = client[mongo['MONGODB_DBNAME']]

    def start_requests(self):
        url = 'http://lishi.tianqi.com/'
        yield scrapy.Request(url, callback=self.get_city)

    def get_city(self, response):
        city_ele = response.xpath('//ul[@class="table_list"]/li/a')
        for city in city_ele:
            city_href = city.xpath('./@href').extract_first()
            yield scrapy.Request(url=self.base_url + city_href, callback=self.city_parse)

    def city_parse(self, response):
        dates = response.xpath('//div[contains(@class,"lishifengxiang")]//li/a')
        for date in dates:
            url = date.xpath('./@href').extract_first()
            yield scrapy.Request(url=url, callback=self.date_parse)

    def date_parse(self, response):
        lis = response.xpath('//div[@class="lishitable"]//ul[2]/li')
        city_str = response.xpath('//div[@class="linegraphtitle"]/text()').extract_first()
        keys = ['city', 'date', 'ht', 'lt', 'weather', 'wind_dir']
        for li in lis:
            weather_data = CityWeather()
            weather = li.xpath('./div//text()').extract()
            if len(weather) < 1:
                continue
            city = [re.search('(\w+)\d{4}年', city_str)[1]]
            datas = city + weather
            for value, key in zip(datas, keys):
                weather_data[key] = value
            weather_data['ht'] = int(weather_data['ht'])
            weather_data['lt'] = int(weather_data['lt'])
            weather_data['date'] = datetime.strptime(weather_data['date'], '%Y-%m-%d')
            yield weather_data
