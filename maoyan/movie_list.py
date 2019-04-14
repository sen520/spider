import json
import requests
from lxml import etree
import xml.etree.cElementTree as ET
import re
from fontTools.ttLib import TTFont

host = 'https://maoyan.com'


def get_movie_info(url):
    res = requests.get(url)
    html = etree.HTML(res.text)
    movie_name = html.xpath('string(//h3/text())')
    movie_o_name = html.xpath('string(//div[@class="ename ellipsis"]/text())')
    movie_abstract = '\n'.join(html.xpath('//div[@class="movie-brief-container"]/ul/li/text()'))
    font_str = \
    re.search(r"""<span class="index-left info-num ">\s+<span class="stonefont">(.*?)</span>\s+</span>""", res.text)[1]
    font_face = html.xpath('//style/text()')[0]
    url = 'http:' + re.search('url\(\'(//vfile.meituan.net/colorstone/.*\.woff)', font_face)[1]
    name = re.search('/colorstone/(.*.woff)\'\) format', font_face)[1]
    # 保存woff字体文件为test.woff
    get_font(url)
    font = TTFont('./fonts/test.woff')
    # font.saveXML('./m.xml')  # 转成xml
    num = get_num(font_str)

    print(num)


def get_num(font_str):
    baseFonts = TTFont('./fonts/font.woff')
    base_fonts = ['uniF27B', 'uniE296', 'uniE732', 'uniEFDF',
                  'uniF3AB', 'uniF8EC', 'uniEF37', 'uniE7EE', 'uniE5C5', 'uniEBD9']
    base_nums = ['9', '5', '1', '8', '3', '2', '0', '3', '4', '7', '6']
    online_fonts = TTFont('./fonts/test.woff')
    uni_list = online_fonts.getGlyphNames()[1:-1]
    temp = {}
    for i in range(10):
        onlineGlyph = online_fonts['glyf'][uni_list[i]]
        for j in range(10):
            baseGlyph = baseFonts['glyf'][base_fonts[j]]
            if onlineGlyph == baseGlyph:
                temp["&#x" + uni_list[i][3:].lower() + ';'] = base_nums[j]
    pat = '(' + '|'.join(temp.keys()) + ')'
    num = re.sub(pat, lambda x: temp[x.group()], font_str)
    return num


def get_font(url):
    res = requests.get(url)
    with open('./fonts/test.woff', 'wb') as f:
        f.write(res.content)


if __name__ == '__main__':
    res = requests.get('https://maoyan.com/board')
    html = etree.HTML(res.text)
    movie_hrefs = html.xpath('//p[@class="name"]/a/@href')
    for href in movie_hrefs:
        url = host + href
        get_movie_info(url)
        break
