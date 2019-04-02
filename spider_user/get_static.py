"""
@File  : get_static.py
@Author: sen
@Date  : 2018/7/7 8:30
@Software  : PyCharm
"""
import random
from lxml import etree
import requests


def get_static(path):
    # 建立空列表用于存储获取静态文件的信息
    list = []

    # 打开文件
    with open(path, 'r') as info_get:

        # 循环
        while True:

            # 采用读取行的方式，用于分开每条信息
            info = info_get.readline().strip()

            # 将获取到的信息存放到列表中
            list.append(info)

            # 当文件读取到空行的时候，说明读取到结尾，退出循环并返回列表
            if info == '':
                break
    index = random.randint(0,len(list)-1)
    return list[index]


def get_html(url,flag=0):
    headers = {
        'User-Agent': get_static('./static/user-agent.txt')
    }
    proxies = {
        "http": get_static('./static/proxy.txt'),
        "https": get_static('./static/https_proxy.txt'),
    }
    if flag == 1 :
        try:
            response = requests.get(url, headers=headers, proxies=proxies,timeout=1)
        except Exception:
            print('代理不可用')
            response = requests.get(url,headers=headers,timeout=1)
        html = response.text
        text = etree.HTML(html)
        return text
    else:
        response = requests.get(url, headers=headers, timeout=1)
        html = response.text
        text = etree.HTML(html)
        return text


# 测试
if __name__ == '__main__':
    info = get_static('./static/user-agent.txt')
    print(info)
    info = get_static('./static/proxy.txt')
    print(info)
