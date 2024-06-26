"""
@File  : spider.py
@Author: sen
@Date  : 2018/7/7 8:45
@Software  : PyCharm
"""
from lxml import etree
import requests

from get_static import get_static, get_html
from save_info import save_mysql


def parse(html):
    name_list = html.xpath('//div[@id="yw1"]/table/tbody/tr/td[2]/a/text()')
    url_list = html.xpath('//div[@id="yw1"]/table/tbody/tr/td[2]/a/@href')
    data_list = html.xpath('//div[@id="yw1"]/table/tbody/tr/td[1]/text()')
    addr_list_province = html.xpath('//*[@id="yw1"]/table/tbody/tr/td[3]/text()')
    addr_list_city = html.xpath('//div[@id="yw1"]/table/tbody/tr/td[4]/text()')
    addr_list_location = html.xpath('//div[@id="yw1"]/table/tbody/tr/td[5]/text()')

    for name, url, data, addr_province, addr_city, addr_localtion in zip(name_list, url_list, data_list,
                                                                         addr_list_province, addr_list_city,
                                                                         addr_list_location):
        item = {}
        item['name'] = name
        item['url'] = url
        item['data'] = data
        item['addr_province'] = addr_province
        item['addr_city'] = addr_city
        item['addr_localtion'] = addr_localtion

        save_mysql(database='spider', item=item)
        html_competion = get_html(url)
        parse_info(html_competion)


def parse_info(html):
    info = html.xpath("//div[@class='col-lg-12 competition-wca']//dl/dd[4]/text()")
    print(info)


if __name__ == '__main__':
    url = 'https://cubingchina.com/competition'
    html = get_html(url)
    # print(html)
    parse(html)
