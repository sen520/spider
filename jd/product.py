import requests
import json
import re
from tools.data_to_json import data_to_json


def get_html(page):
    url = 'https://club.jd.com/discussion/getProductPageImageCommentList.action?productId=7652029&isShadowSku=0&callback=function(){{}}&page={}&pageSize=20&_=1561104446160'.format(
        page)
    res = requests.get(url)
    json_str = re.search('function%28%29%7B%7D\((.*)\)', res.text)
    data = json.loads(json_str[1])
    data_list = []
    for img in data['imgComments']['imgList']:
        data_dict = {
            'url': img['imageUrl'],
            'info': {
                'content': img['commentVo']['content'],
                'create_time': img['commentVo']['creationTime'],
                'product_time': img['commentVo']['referenceTime'],
                'product_color': img['commentVo']['productColor'],
                'product_size': img['commentVo']['productSize'],
                'nick_name': img['commentVo']['nickname'],
                'user_level_name': img['commentVo']['userLevelName'],
                'user_client_show': img['commentVo']['userClientShow'],
            }
        }
        data_list.append(data_dict)
    data_to_json(data_list, 'jd')


if __name__ == '__main__':
    get_html(3)
