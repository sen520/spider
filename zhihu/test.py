import requests
from lxml import etree
import json
from tools.data_to_json import data_to_json


def spider(search, offset):
    url = 'https://www.zhihu.com/api/v4/search_v3?t=general&q={}&lc_idx={}&offset={}&limit=20'.format(search, int(offset)+5, offset)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Cookie': '_zap=65f54203-6b6b-4df6-9695-066d8e4337e4; d_c0="ABCqaE1keg-PTgEaPuVmiT686URGm1DwcuE=|1558691612"; q_c1=0d3a70fa678d4a26858e310dae5cd01c|1558694192000|1558694192000; tgw_l7_route=537a925d07d06cecbf34cd06a153f671; _xsrf=4BmtHg42ZeGowK8G6YjsSIyxWLcsypCf; tst=r; __gads=ID=86004b95131af240:T=1561082991:S=ALNI_MYbzaeVrvNbvcHG7DdETIKgARgAJA; capsion_ticket="2|1:0|10:1561083078|14:capsion_ticket|44:M2FiOTNiZGZiZDE3NDY3M2FmNmM0ZDIxMDlmZmY3ZTE=|75625d2d454a6cc6c40fb7597e027b64ed82e79a4c32cd7207476e841cae21cf"; __utma=51854390.1681338791.1561083165.1561083165.1561083165.1; __utmb=51854390.0.10.1561083165; __utmc=51854390; __utmz=51854390.1561083165.1.1.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/wind_white/article/details/77851577; l_n_c=1; l_cap_id="ZTIwYzQxMmMwYTk2NGVhMmE0NjEzMmFlNjZiOTk4ZjA=|1561083171|21e52a7f9d68f1bc55d79afe2b8f468e4fe0ad12"; r_cap_id="YjU5NDU0MjUxNWQ2NDAwMmE3YzJhYzRhYTI1MjA1NWU=|1561083171|de07e94d4cfbb24354062a756e83cd8cf746a4cd"; cap_id="ZTJlNTAyNWI5ZmZlNGFhYTk0ODVmM2FkMjg0NTgxOWU=|1561083171|05d34ffbcad1383cb1a441e42396bd703adba156"; n_c=1; __utmv=51854390.000--|2=registration_date=20170305=1^3=entry_date=20190524=1',
        'Host': 'www.zhihu.com',
    }
    res = requests.get(url, headers=headers)
    data = json.loads(res.text)
    data_list = []
    for d in data['data']:
        hot_list = []
        try:
            for hot in d['object']['content_hot_list']:
                hot_dict = {
                    'title': hot['title'],
                    'related_img': hot['avatar_url']
                }
                hot_list.append(hot_dict)
        except:
            pass
        try:
            print(d['highlight'])
            data_dict = {
                'highlight': d['highlight'],
                'content_hot_list': hot_list
            }
            if data_dict['highlight'] != {}:
                data_list.append(data_dict)
        except:
            pass
    data_to_json(data_list, 'zhihu')


if __name__ == '__main__':
    spider('手机', 40)
