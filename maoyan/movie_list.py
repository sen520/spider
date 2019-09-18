import json
import requests
from lxml import etree
import xml.etree.cElementTree as ET
import re
from fontTools.ttLib import TTFont

host = 'https://maoyan.com'


def get_movie_info(url, headers):
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)

    #  电影名
    movie_name = html.xpath('string(//h3/text())')

    # en/zh 名字
    movie_o_name = html.xpath('string(//div[@class="ename ellipsis"]/text())')

    # 简介：分类，区域，时长，上映日期
    movie_abstract = '\n'.join(html.xpath('//div[@class="movie-brief-container"]/ul/li/text()'))
    print(movie_abstract.split('\n\n')[0])
    tag = movie_abstract.split('\n\n')[0].split(',')
    abstract = movie_abstract.split('\n\n')[1].strip()
    # 用户评分
    font_str = \
        re.search(r"""<span class="index-left info-num ">\s+<span class="stonefont">(.*?)</span>\s+</span>""",
                  res.text)[1]
    font_face = html.xpath('//style/text()')[0]
    # 字体链接
    url = 'http:' + re.search('url\(\'(//vfile.meituan.net/colorstone/.*\.woff)', font_face)[1]
    # 字体文件名
    # name = re.search('/colorstone/(.*.woff)\'\) format', font_face)[1]
    # 保存woff字体文件为test.woff
    get_font(url)
    # font = TTFont('./fonts/' + name)
    # font.saveXML('./m.xml')  # 转成xm
    stars = get_num(font_str)
    # 参评分人数
    person_num_str = re.search('<span class=\'score-num\'><span class="stonefont">(.*)</span>人评分</span>', res.text)[1]
    person_num = get_num(person_num_str)

    # 累计票房
    movie_box_str = re.search(
        '<div class="movie-index-content box">\s+<span class="stonefont">(.*)</span><span class="unit">(.*)</span>\s+</div>',
        res.text)
    movie_box = get_num(movie_box_str[1]) + movie_box_str[2]

    # 热门短评
    # comments_divs = html.xpath('//div[@class="comment-list-container"]//li')
    comments_persons = html.xpath('//div[@class="user"]/span[@class="name"]/text()')
    comments_times = html.xpath('//div[@class="time"]/span/text()')
    comments_approves = html.xpath('//div[@class="approve "]/span/text()')
    comments_texts = html.xpath('//div[@class="comment-content"]/text()')
    comments_list = []
    for comments_person, comments_time, comments_approve, comments_text in zip(comments_persons, comments_times,
                                                                               comments_approves, comments_texts):
        comment_dict = {
            'user': comments_person,
            'time': comments_time,
            'approve': comments_approve,
            'comment': comments_text,
        }
        comments_list.append(comment_dict)

    data_dict = {
        'name': movie_name,
        'other_name': movie_o_name,
        'abstract': {
            'tag': tag,
            'abstract': abstract
        },
        'stars': {
            'num': person_num,
            'result': stars
        },
        'movie_box': movie_box,
        'comments': comments_list,
    }
    return  data_dict

def save_movie(data_list, name):
    with open(name + '.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data_list, indent=2, ensure_ascii=False, separators=(',', ': ')))


def get_num(font_str):
    """
    通过比较已有的woff对应的font值，确定获取到的font的值
    :param font_str: 获取到的font值
    :return: 解析出的数字
    """
    baseFonts = TTFont('./fonts/font.woff')
    base_fonts = ['uniF130', 'uniF357', 'uniE595', 'uniF88B',
                  'uniE05E', 'uniEA85', 'uniEF99', 'uniF6B4', 'uniF732', 'uniEE60']
    base_nums = ['9', '5', '1', '8', '2', '0', '3', '4', '7', '6']
    online_fonts = TTFont('./fonts/data.woff')
    uni_list = online_fonts.getGlyphNames()[1:-1]
    temp = {}
    online_fonts.saveXML('a.xml')
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
    """
    保存woff文件
    :param url:
    :return:
    """
    res = requests.get(url)
    with open('./fonts/data.woff', 'wb') as f:
        f.write(res.content)



if __name__ == '__main__':
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "_lxsdk_cuid=16c83c24021c8-004738fc119f25-396a4507-1fa400-16c83c24021c8; uuid_n_v=v1; uuid=B28F9740D9DF11E98CE175A6C6B4C416EE55972FC64D4510A2F83D5F2A829843; _csrf=071e678edd5f1a19a1193275add0b106101e3d0032351f8fcb8cba6e7159e37b; _lxsdk=B28F9740D9DF11E98CE175A6C6B4C416EE55972FC64D4510A2F83D5F2A829843; __mta=146061963.1565578642053.1568789112216.1568789191408.4; _lxsdk_s=16d431d0b6f-8b5-d1-c97%7C%7C6",
        "Host": "maoyan.com",
        "Pragma": "no-cache",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    res = requests.get('https://maoyan.com/board', headers=headers)
    html = etree.HTML(res.text)
    movie_hrefs = html.xpath('//p[@class="name"]/a/@href')
    print(movie_hrefs)
    movies_list = []
    for href in movie_hrefs:
        url = host + href
        movie_dict = get_movie_info(url, headers)
        movies_list.append(movie_dict)
    save_movie(movies_list, 'movie')
