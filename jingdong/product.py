from uuid import uuid4
import requests
from lxml import etree
import time
import json


def send_request(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.content


def next_request(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.content


def get_info(html_str):
    html = etree.HTML(html_str)
    imgs = html.xpath('//div[@class="p-img"]/a/img/@source-data-lazy-img')
    hrefs = html.xpath('//div[@class="p-img"]/a/@href')
    titles = html.xpath('//div[@class="p-img"]/a/@title')
    prices = html.xpath('//div[@class="p-price"]/strong/i')
    l = []
    for img, href, title, price in zip(imgs, hrefs, titles, prices):
        l.append({'href': href, 'title': title, 'price': price.xpath('string(.)')})
    return l


if __name__ == '__main__':
    data_list = []
    for i in range(1, 196, 2):
        url = 'https://search.jd.com/Search?keyword=手机&enc=utf-8&page=' + str(i)
        html_str = send_request(url)
        l = get_info(html_str)
        next_url = 'https://search.jd.com/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&s=' + str(
            1 + i * 56) + '&cid3=655&page=' + str(
            i) + '&scrolling=y&log_id=' + str(time.time()) + '&tpl=3_M'
        html_str = next_request(url)
        l.extend(get_info(html_str))
        data_list.extend(l)
        print(i)
        print('=======================')
        with open('phone.json', 'w', encoding='utf8') as f:
            f.write(json.dumps(data_list, indent=2, ensure_ascii=False, separators=(',', ': ')))
    #     with open('./img/'+ uuid4().hex + '.jpg', 'wb') as f:
    #         f.write(requests.get('http:'+i).content)
