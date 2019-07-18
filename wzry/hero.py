import requests
from lxml import etree

url = 'https://db.18183.com/wzry/'
res = requests.get(url)
html = etree.HTML(res.text)
url = html.xpath('//div[@class="section hero-result-box mod-bg clearfix"]/ul[@class="mod-iconlist"]/li/a/@href')
url_list = ['https://db.18183.com/' + x for x in url]
for u in url_list:
    print(u)