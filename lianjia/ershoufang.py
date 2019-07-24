import requests
from lxml import etree
import re
from tools.data_to_json import data_to_json, parse_price, sort_dict
import time

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "select_city=340100; all-lj=3d8def84426f51ac8062bdea518a8717; lianjia_ssid=d301dfea-1bb4-4f61-b0d5-59d848c45755; lianjia_uuid=2ee102e0-45c6-4262-82e9-f4e0abd52e46; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1563930968; _smt_uid=5d37b15b.24b9bbdc; UM_distinctid=16c218ccdf2488-03d045b900d0a9-3a65420e-1fa400-16c218ccdf33f7; CNZZDATA1254525948=693588990-1563926787-%7C1563926787; CNZZDATA1255633284=1625222333-1563929039-%7C1563929039; CNZZDATA1255604082=660467272-1563926875-%7C1563926875; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiODgwZTI5YmQ1OTA5ZDM2YTUwMWYxZDBjY2ZkMjM3YzUxNzUzYjEyMTVjYWQ4Y2YxMGViNDVmNzU3OTVjYmI2OTJkMzExYjEyMzk2ZGZlZWJmMzY4MGExYWZjYTdjMzY0MzNhZGU3MzJmNzBmNTBlYzQ0ZmM3MDBkMjg5YWZjZDFjN2FjZDBjYTY0YjJiZTAwYmJiYjJhM2Y1NGIwZWM2NjFjNDY1OGMwZjEwYzFkMWQyZWVmNDZjMzkxNDllNjc4MTNmMWFjYzk2M2E1MmNjNTczYmQzZDExYmU3M2U2NjQ5ZTRmMGY4ZDM3NzExY2M3ODcwNjFjOGZhZjY0MzUwYzBmMWMyNDM5MThjODU2NTRjZTBhNmE2MDQ4MDAwMDMzMzBjMDZiYTNjMWE4MWVjMmQwZjM0ODQ4NzkwNDVlZjFcIixcImtleV9pZFwiOlwiMVwiLFwic2lnblwiOlwiMmExNzNmOGFcIn0iLCJyIjoiaHR0cHM6Ly9oZi5saWFuamlhLmNvbS9lcnNob3VmYW5nL3BnMS8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216c218ced74c-0e152e4661837-3a65420e-2073600-16c218ced7533a%22%2C%22%24device_id%22%3A%2216c218ced74c-0e152e4661837-3a65420e-2073600-16c218ced7533a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _qzjc=1; _jzqa=1.2596822940614686000.1563930982.1563930982.1563930982.1; _jzqc=1; _jzqckmp=1; _ga=GA1.2.1915187137.1563930989; _gid=GA1.2.973729598.1563930989; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1563931150; _qzja=1.1038437307.1563930980799.1563930980799.1563930980799.1563930980799.1563931149801.0.0.0.2.1; _qzjb=1.1563930980799.2.0.0.0; _qzjto=2.1.0; _jzqb=1.2.10.1563930982.1",
    "Host": "hf.lianjia.com",
    "Pragma": "no-cache",
    "Referer": "https://hf.lianjia.com/ershoufang/pg1/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "X-Tingyun-Id": "gVpxXPG41PA;r=931149937",
}


def parse_first_page(url, info_dict):
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)
    lis = html.xpath('//ul[@class="sellListContent"]/li')
    for li in lis:
        a = li.xpath('.//div[@class="title"]/a/@href')
        detail_res = requests.get(a[0], headers=headers)
        time.sleep(1)
        detail_html = etree.HTML(detail_res.text)
        city = detail_html.xpath('string(//span[@class="info"]/a)')
        area = li.xpath('.//div[@class="houseInfo"]/a/text()')[0]
        price = li.xpath('string(.//div[@class="totalPrice"])')
        single_price = li.xpath('.//div[@class="unitPrice"]/span/text()')[0]
        price = int(parse_price(price))
        single_price = int(re.search('\d+', single_price)[0])
        if city not in info_dict.keys():
            info_dict[city] = []
        info_dict[city].append({'area': area, 'price': price, 'single_price': single_price})
        print({'area': area, 'price': price, 'single_price': single_price})
        info_dict = sort_dict(info_dict, 'single_price')
    return info_dict


if __name__ == '__main__':
    info_dict = {}
    name_list = []
    for i in range(1, 101):
        url = 'https://hf.lianjia.com/ershoufang/pg{}/'.format(i)
        info_dict = parse_first_page(url, info_dict)
        print(i)
        time.sleep(1)
        data_to_json(info_dict, 'house')
