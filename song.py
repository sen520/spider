import operator
from datetime import datetime
import logging
import requests
from lxml import etree
import re
import json
from urllib.parse import unquote


def get_comments(id):
    url = 'http://comment.kuwo.cn/com.s?type=get_comment&uid=0&prod=newWeb&digest=15&sid={}&page=1&rows=100&f=web&jpcallback=getCommentListFn&_=1554970861861'.format(
        id)
    res = requests.get(url)

    a = re.search('var jsondata=({.*,"comment_tpye":"normal","total":"\d+"})', res.text)[1]
    o = json.loads(a)
    return o['rows']

def create_logger(name):
    log = logging.getLogger(name)
    log.handlers = []
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.FileHandler(name))
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    log.addHandler(stream_handler)
    return log

if __name__ == '__main__':

    res = requests.get(url='http://www.kuwo.cn/bang/index')
    html = etree.HTML(res.text)

    song_name = html.xpath('//ul[@class="listMusic"]/li/div[@class="name"]/a/text()')
    urls = html.xpath('//ul[@class="listMusic"]/li/div[@class="name"]/a/@href')
    song_list = []
    for name, url in zip(song_name, urls):
        id = re.search('/(\d+)\?', url)[1]
        try:
            rows = get_comments(id)
        except Exception as e:
            log = create_logger('./error.log')
            log.error(e)
            log.error(datetime.now())
            continue
        comment = []
        for row in rows:
            # print(row)
            user = unquote(row['u_name'], encoding="utf-8")
            msg = row['msg']
            date = row['time']
            like_num = int(row['like_num'])
            comment.append({'user': user, 'msg': msg, 'date': date, 'like_num': like_num})
            # comment.append({'user': user, 'msg': msg, 'date': datetime.strptime(date, "%Y-%m-%d %H:%M:%S"), 'like_num': like_num})
        comment.sort(key=operator.itemgetter('like_num'), reverse=True)
        song_dict = {
            'name': name,
            'url': url,
            'comments': comment
        }
        song_list.append(song_dict)
        print(song_list)
        with open('a.json', 'w', encoding='utf8') as f:
            f.write(json.dumps(song_list, indent=2, ensure_ascii=False, separators=(',', ': ')))