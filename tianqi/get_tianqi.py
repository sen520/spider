from datetime import datetime

import requests
from lxml import etree
import time
from tools.tools import data_to_json, write_csv, create_logger
import os

log = create_logger('spider.log')

headers = {
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


def get_list_page():
    city_list = []
    url = 'http://lishi.tianqi.com/'
    res = requests.get(url, headers=headers)
    res.encoding = 'gbk'
    html = etree.HTML(res.text)
    city_ele = html.xpath('//ul[@class="bcity"]/li/a[contains(@href, "http")]')
    for city in city_ele:
        city_name = city.xpath('./text()')[0]
        city_href = city.xpath('./@href')[0]
        city_list.append({'name': city_name, 'href': city_href})

    return city_list


def get_city_page(city):
    res = requests.get(city['href'], headers=headers)
    res.encoding = 'gbk'
    html = etree.HTML(res.text)
    dates = html.xpath('//div[@class="tqtongji1"]//li/a')
    date_list = []
    for date in dates:
        date_time = date.xpath('./text()')[0]
        url = date.xpath('./@href')[0]
        date_list.append({'date': date_time, 'url': url})
    return date_list


def get_data(date):
    res = requests.get(date['url'], headers=headers)
    res.encoding = 'gbk'
    html = etree.HTML(res.text)
    uls = html.xpath('//div[@class="tqtongji2"]//ul')

    datas = []
    for ul in uls:
        li = ul.xpath('./li//text()')
        if li[0] == '日期':
            continue
        else:
            log.info(datetime.now())
            log.info(li)
            if len(li) == 6:
                datas.append(
                    {'date': li[0], 'ht': li[1], 'lt': li[2], 'weather': li[3], 'wind_dir': li[4], 'wind_value': li[5]})
            else:
                try:
                    if li[4] == '暂无实况':
                        datas.append(
                            {'date': li[0], 'ht': li[1], 'lt': li[2], 'weather': li[3], 'wind_dir': '', 'wind_value': 0})
                except Exception as e:
                    log.error(e)
                    if li[1] == li[2]:
                        datas.append(
                            {'date': li[0], 'ht': li[1], 'lt': li[2], 'weather': '', 'wind_dir': '',
                             'wind_value': 0})
                    else:
                        try:
                            datas.append({'date': li[0], 'ht': li[1], 'lt': li[2], 'weather': li[3], 'wind_dir': '', 'wind_value': 0})
                        except:
                            datas.append({'date': li[0], 'ht': li[1], 'lt': li[2], 'weather': '', 'wind_dir': '', 'wind_value': 0})

    return datas


if __name__ == '__main__':
    city = get_list_page()
    data = []
    total = len(city)
    for index, c in enumerate(city):
        print('一共%d, 正在抓取第%d' %(total, index))
        print(c['name'])
        if c['name'] + '.csv' in os.listdir('./data'):
            continue
        date_list = get_city_page(c)
        page_list = []
        for date in date_list:
            page_list += get_data(date)
            time.sleep(1)
        write_csv('./data/'+c['name'], page_list)
        time.sleep(1)
