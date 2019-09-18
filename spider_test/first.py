import requests
from lxml import etree
import json
import time

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


def css_spider(session):
    url = 'http://glidedsky.com/level/web/crawler-css-puzzle-1'
    res = session.get(url)
    html = etree.HTML(res.text)
    html.xpath('')


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
                print(ip)
                proxy = {
                    'http': ip,
                    'https': ip
                }
                url = 'http://glidedsky.com/level/web/crawler-ip-block-1?page=' + str(i)
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



if __name__ == '__main__':
    email = ''
    pwd = ''
    session = login(email, pwd)
    # css_spider(session)
    ip_spider(session)
