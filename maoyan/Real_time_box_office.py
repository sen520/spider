import requests
import json

res = requests.get('https://box.maoyan.com/promovie/api/box/second.json')
json_obj = json.loads(res.text)
data = json_obj['data']
movie_list = data['list']

for i in movie_list:
    name = i['movieName'] # 电影名
    num = i['boxInfo']  # 票房
    seat = i['avgSeatView'] # 上座率
    print(name, num, seat)