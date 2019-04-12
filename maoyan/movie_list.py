import requests
from lxml import etree


host = 'https://maoyan.com'

def get_movie_info(url):
    res = requests.get(url)
    html = etree.HTML(res.text)
    movie_name = html.xpath('string(//h3/text())')
    movie_o_name = html.xpath('string(//div[@class="ename ellipsis"]/text())')
    movie_abstract = '\n'.join(html.xpath('//div[@class="movie-brief-container"]/ul/li/text()'))
    x = html.xpath('//div[@class="movie-index-content score normal-score"]/span/span/text()')
    # for i in x:
    print(x)

if __name__ == '__main__':
    res = requests.get('https://maoyan.com/board')
    html = etree.HTML(res.text)
    movie_hrefs = html.xpath('//p[@class="name"]/a/@href')
    for href in movie_hrefs:
        url = host + href
        get_movie_info(url)
        break