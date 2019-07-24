import requests
from lxml import etree
from pypinyin import lazy_pinyin
from tools.tools import data_to_json
import json


def get_hotel(city):
    try:
        with open('./city.json', encoding='utf-8') as f:
            city_dict = json.loads(f.read())
    except:
        city_dict = get_city()
    city_id = city_dict[city]
    city_pinyin = ''.join(lazy_pinyin(city)).title()
    url = 'https://hotels.ctrip.com/Domestic/Tool/AjaxIndexHotSaleHotelNew.aspx?traceid=8288828572670897460'
    form_data = {
        'city': city_id,
        'cityName': city,
        'cityPY': city_pinyin,
        'psid': ''
    }
    res = requests.post(url, data=form_data)
    html = etree.HTML(res.text)
    hotels = html.xpath('//ul')
    hotel_data = []
    for hotel in hotels:
        hotel_img_get = hotel.xpath('.//li[@class="hotel_pic"]/a/img/@src')
        hotel_img =list(map(lambda x: 'https:' + x, hotel_img_get))
        hotel_name_get = hotel.xpath('.//h3//text()')
        hotel_name = ''.join(list(map(lambda x: x.strip(), hotel_name_get)))
        hotel_type_get = hotel.xpath('.//li/span//@title')
        hotel_type = list(map(lambda x: x.strip(), hotel_type_get))
        hotel_address_get = hotel.xpath('.//div[@class="searchresult_htladdress"]/a/text()')
        hotel_address = list(map(lambda x: x.strip(), hotel_address_get))
        hotel_commet_get = hotel.xpath('.//span[@class="brief_comment_text"]/text()')
        hotel_commet = '\n'.join(list(map(lambda x: x.strip(), hotel_commet_get)))
        hotel_score = hotel.xpath('string(.//a[@class="hotel_comment J_trace_hotHotel"])')
        hotel_dict = {
            'hotel_img': hotel_img,
            'hotel_name': hotel_name,
            'hotel_type': hotel_type,
            'hotel_address': hotel_address,
            'hotel_commet': hotel_commet,
            'hotel_score': hotel_score,
        }
        hotel_data.append(hotel_dict)
    data_to_json(hotel_data, 'hotel')


def get_city():
    url = 'https://hotels.ctrip.com/'
    res = requests.get(url)
    html = etree.HTML(res.text)
    print(res.text)
    tag_as = html.xpath('//ul[@id="hotsold_city_list"]/li/a')
    city_dict = {}
    for tag_a in tag_as:
        city = tag_a.xpath('string(./text())')
        if city == '更多':
            continue
        id = tag_a.xpath('string(./@data-id)')
        city_dict[city] = id
    more_tags = html.xpath('//div[@id="pop_box_city"]/a')
    for more_tag in more_tags:
        city = more_tag.xpath('string(./text())')
        if city == '×':
            continue
        id = more_tag.xpath('string(./@data-id)')
        city_dict[city] = id
    data_to_json(city_dict, 'city')
    return city_dict


if __name__ == '__main__':
    # city = input('请输入想查询的城市：')
    city = '北京'
    get_hotel(city)
