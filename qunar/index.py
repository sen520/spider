import requests
import json
from tools.tools import data_to_json


def get_low_inland():
    low_inland_url = 'https://ws.qunar.com/lowerPrice.jcp?&callback=function(){}'
    res = requests.get(low_inland_url)
    data = json.loads(res.text)
    data_list = []
    for from_city in data['data'].keys():
        record_list = []
        records = data['data'][from_city]['records']
        for record in records:
            record_dict = {
                'date': record['date'],
                'price': record['price'],
                'discount': record['discount'],
                'arrCity': record['arrCity'],
            }
            record_list.append(record_dict)
        data_dict = {
            from_city: record_list
        }
        data_list.append(data_dict)
    data_to_json(data_list, 'qunar_inland')


def get_abroad(from_city):
    abroad_url = 'https://ws.qunar.com/lpisearchd?callback=function(){{}}&from={}&to=Hot&month=All&cachefrom=&cacheto=&type=rt&source=thome&_=1561107214141'.format(
        from_city)
    res = requests.get(abroad_url)
    data = json.loads(res.text)
    data_list = []
    for d in data['data']:
        data_dict = {
            "from": from_city,
            "info": {
                'to': d['fto'],
                'from_time': d['dtime'],
                'to_time': d['atime'],
                'price': d['price'],
            }
        }
        data_list.append(data_dict)
    data_to_json(data_list, 'qunar_abroad')

if __name__ == '__main__':
    # get_low_inland()
    get_abroad('上海')
