import io
import json
import operator
import re

import pandas as pd
import requests
import os


def data_to_json(data, name):
    with io.open(name + '.json', 'w', encoding='utf-8') as fo:
        fo.write(json.dumps(data, ensure_ascii=False, indent=2, separators=(',', ': ')))


def sort_dict(data, field):
    """
    sort dict
    :param data: [dict] the data to sort
    :param field: the field to sort
    :return:
    """
    for key, value in data.items():
        data[key] = sorted(value, key=operator.itemgetter(field))
    return data


def parse_price(num_str):
    """
    parse price
    :param num_str: [string] string of price
    :return: [float] num of price
    """
    try:
        result = re.search('(\d+\.*\d*)(.*)', num_str)
        num = float(result[1])
        unit = result[2]
        if re.search('万', unit):
            num *= 10000
        if re.search('千', unit):
            num *= 1000
        if re.search('百', unit):
            num *= 1000
        if re.search('亿', unit):
            num *= 100000000
        return num
    except Exception as e:
        print(e)
        return num_str


def get_img(url, path, name=None):
    if not name:
        name = url.split('/')[-1]
    path = os.path.join(path, name)
    res = requests.get(url)
    with open(path, 'wb') as f:
        f.write(res.content)
    return path


class GetProxy(object):
    def __init__(self):
        self.proxy_url = 'http://api.ip.data5u.com/dynamic/get.html?order=c77bcb61b876d0efe082d749462f13a7&json=1&sep=3'

    def get_proxy(self):
        res = requests.get(self.proxy_url)
        proxy_data = json.loads(res.text)
        if proxy_data['msg'] == 'ok':
            proxy_dict = proxy_data['data'][0]
            proxy = proxy_dict['ip'] + ':' + str(proxy_dict['port'])
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }
            res = requests.get('https://www.baidu.com', proxies=proxies)
            print(res.status_code)
            if res.status_code == 200:
                return proxies


def get_proxy():
    proxy = GetProxy()
    return proxy.get_proxy()


def data_to_csv(data_list, csv_key, name):
    """
    save data to csv
    :param data_list: data
    :param csv_key: csv column
    :param name: file name
    :return:
    """
    final_data = []
    for data in data_list:
        sign_key = []
        for key, value in data.items():
            sign_key.append(value)
        final_data.append(sign_key)
    # 将总数据转化为data frame再输出
    df = pd.DataFrame(data=final_data,
                      columns=csv_key)
    df.to_csv(name + '.csv', index=False, encoding='utf-8_sig')


if __name__ == '__main__':
    proxy = get_proxy()
    print(proxy)
