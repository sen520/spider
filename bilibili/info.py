import requests
import re
from lxml import etree

headers = {
    "Access-Control-Request-Headers": "range",
    "Access-Control-Request-Method": "GET",
    "Origin": "https://www.bilibili.com",
    "Referer": "https://www.bilibili.com/video/av60510746",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "e": "ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEVEuxTEto8i8o859r1qXg8xNEVE5XREto8GuFGv2U7SuxI72X6fTr859r1qXg8gNEVE5XREto8z5JZC2X2gkX5L5F1eTX1jkXlsTXHeux_f2o859IB_",
    "deadline": "1563956237",
    "gen": "playurl",
    "nbs": "1",
    "oi": "604479277",
    "os": "bsyu",
    "platform": "pc",
    "trid": "ac13b2ca00c24928a6369260ca190dbd",
    "uipk": "5",
    "upsig": "06bf108ee3931591e77e4d74a9ba7066",
    "uparams": "e,deadline,gen,nbs,oi,os,platform,trid,uipk",
    "mid": "0",
}


def get_cid(url):
    res = requests.get(url, headers=headers)
    res.encoding = 'uft-8'
    html = etree.HTML(res.text)
    cid = re.search('"cid":(\d+)', res.text)[1]
    name = html.xpath('//h1/@title')[0]
    return cid, name


def get_comments(url, name):
    res = requests.get(url)
    res.encoding = 'uft-8'
    text = res.text.replace('encoding="UTF-8"', '')
    html = etree.HTML(text)
    bullet_screen = html.xpath('//d/text()')
    data = {'name': name, 'bullet_screen': bullet_screen}
    print(data)


if __name__ == '__main__':
    url = 'https://www.bilibili.com/video/av60116769/?spm_id_from=333.334.b_63686965665f7265636f6d6d656e64.16'
    cid, name = get_cid(url)
    comment_url = 'https://comment.bilibili.com/{}.xml'.format(cid)
    get_comments(comment_url, name)
