import requests
from lxml import etree
import json
import time
import re
import base64
from fontTools.ttLib import TTFont

main_url = 'http://glidedsky.com/'
session = requests.session()


def login(email, pwd):
    url = 'http://glidedsky.com/login'
    res = session.get(url)
    login_html = etree.HTML(res.text)
    token = login_html.xpath('//input[@name="_token"]/@value')[0]
    data = {'_token': token, 'email': email, 'password': pwd}
    session.post('http://glidedsky.com/login', data=data)
    return session


def get_proxy():
    url = ''
    res = requests.get(url)
    data = json.loads(res.text)
    ip = data['data'][0]['ip'] + ':' + str(data['data'][0]['port'])
    return ip


def ip_spider(session):
    sum_num = 0
    ip_list = []
    for i in range(1, 1001):
        while True:
            try:
                while True:
                    ip = get_proxy()
                    if ip not in ip_list:
                        ip_list.append(ip)
                        break
                    time.sleep(3)
                proxy = {
                    'http': ip,
                    'https': ip
                }
                url = 'http://glidedsky.com/level/web/crawler-ip-block-2?page=' + str(i)
                res = session.get(url, proxies=proxy, timeout=5)
                html = etree.HTML(res.text)
                list = html.xpath('//div[@class="row"]/div/text()')
                if len(list) == 0:
                    continue
                sum_num += sum(map(lambda i: int(i.strip()), list))
                print(sum_num)
                break
            except Exception as e:
                print(e)


def font_spider(session):
    sum_num = 0
    for i in range(1, 1001):
        print(i)
        res = session.get('http://glidedsky.com/level/web/crawler-font-puzzle-1?page=' + str(i))
        font_base = re.search('src: url\(data:font;charset=utf-8;base64,(.*)\) format\("truetype"\);', res.text)
        font_b = base64.b64decode(font_base[1])
        with open('./data/test.ttf', 'wb') as f:
            f.write(font_b)
        font = TTFont(io.BytesIO(font_b))
        bestcmap = font['cmap'].getBestCmap()
        newmap = dict()
        for key in bestcmap.keys():
            value = bestcmap[key]
            key = hex(key)
            newmap[key] = value
        print(newmap)
        response_ = res.text
        for key, value in newmap.items():
            key_ = key.replace('0x', '&#x') + ';'
            if key_ in response_:
                response_ = response_.replace(key_, str(value))
        html = etree.HTML(res.text)
        num_list = html.xpath('//div[@class="row"]/div/text()')
        num_list = [int(num.strip()) for num in num_list]
        print(num_list)
        for num in num_list:
            sum_num += num
    print(sum_num)



if __name__ == '__main__':
    email = ''
    pwd = ''
    session = login(email, pwd)
    # ip_spider(session)
    font_spider(session)
