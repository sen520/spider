import requests
from lxml import etree
import pymongo
import pymysql

def send_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    html = etree.HTML(response.text)
    return html

def parseAndSave(html,wb):
    title_list = html.xpath('//div[@class="list-info"]/h2[@class="title"]/a/text()')
    price_list = html.xpath('//p[@class="sum"]/b/text()')
    unit_price_list = html.xpath('//div[@class="price"]/p[2]/text()')
    community_list = html.xpath('//div[@class="jjrinfo"]/span[1]/text()')
    hourse_info_list1 = html.xpath('//p[@class="baseinfo"]/span[1]/text()')
    hourse_info_list2 = html.xpath('//p[@class="baseinfo"]/span[2]/text()')
    hourse_info_list3 = html.xpath('//p[@class="baseinfo"]/span[3]/text()')
    hourse_info_list4 = html.xpath('//p[@class="baseinfo"]/span[4]/text()')
    hourse_info_list = []
    for h1, h2, h3, h4 in zip(hourse_info_list1, hourse_info_list2, hourse_info_list3, hourse_info_list4):
        str = h1 + '\n' + h2 + '\n' + h3 + '\n' + h4
        hourse_info_list.append(str)
    addr_list = html.xpath('//p[@class="baseinfo"]/span[1]/a[1]/text()')

    for title, price, unit_price, community, hourse_info, addr in zip(title_list, price_list,
                                                                      unit_price_list, community_list,
                                                                      hourse_info_list,
                                                                      addr_list):
        item = {}
        item['title'] = title
        item['price'] = float(price) * 10000
        item['unitPrice'] = int(unit_price[0:-3])
        item['community'] = community
        item['hourseInfo'] = hourse_info.strip()
        item['floor'] = ''
        item['addr'] = addr
        sql = 'insert into t_hf VALUES (0,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql,
                            [item['title'], item['price'], item['unitPrice'], item['community'], item['hourseInfo'],
                             item['floor'], item['addr']])
        client.commit()
        # wb.insert_one(dict(item))







if __name__ == '__main__':
    # client = pymongo.MongoClient('localhost', 27017)
    # wb = client.room.njlianjia
    client = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="room",
                             charset="utf8")
    cursor = client.cursor()

    for i in range(1,101):
        print('正在抓取第%s页'%i)
        url = 'https://hf.58.com/ershoufang/pn'+ str(i)
        html = send_request(url)
        parseAndSave(html,cursor)
        print('第%s页存储成功'%i)
    cursor.close()
    client.close()






