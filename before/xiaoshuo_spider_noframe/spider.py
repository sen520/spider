"""
@File  : spider.py
@Author: sen
@Date  : 2018/7/7 9:29
@Software  : PyCharm
"""
from lxml import etree
import requests
import pymysql
import time


# ------------------------------保存文件------------------------------
def save_file(item):
    with open('./static/' + item['book_name'] + '.txt', 'a', encoding="utf-8") as file:
        file.write(item['chapter']+'\n')
        file.write(item['content'])
    return


# ------------------------------获取html对象------------------------------
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    }
    response = requests.get(url=url, headers=headers)
    html = response.text
    text = etree.HTML(html)
    return text


# ------------------------------保存到mysql------------------------------
def save_MySQL(book_list):
    client = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="spider",
                             charset="utf8")
    cursor = client.cursor()
    sql = 'insert into t_book values (0,%s,%s,%s,%s)'
    cursor.execute(sql, [book_list[0], book_list[1], book_list[2], book_list[3]])
    client.commit()
    cursor.close()
    client.close()


# ------------------------------主函数------------------------------
def parse(html):
    for num in range(3, 11):
        type = html.xpath("//div[@class='nav']/ul/li[" + str(num) + ']/a/text()')[0]
        url_get = html.xpath("//div[@class='nav']/ul/li[" + str(num) + ']/a/@href')[0]
        url = 'https:' + url_get
        print('抓取 %s 界面'%type)
        html = get_html(url)
        # 分类列表页面
        url_list = html.xpath('//div[@id="newscontent"]/div[1]/ul/li/span[1]/a/@href')
        bookname_list = html.xpath('//div[@id="newscontent"]/div[1]/ul/li/span[1]/a/text()')
        latest_chapter_list = html.xpath('//div[@id="newscontent"]/div[1]/ul/li/span[2]/a/text()')
        author_list = html.xpath('//div[@id="newscontent"]/div[1]/ul/li/span[3]/text()')

        for url, bookname, latest_chapter, author in zip(url_list, bookname_list, latest_chapter_list, author_list):
            book_list = []
            book_list.append(type)
            book_list.append(bookname)
            book_list.append(author)
            book_list.append(latest_chapter)
            book_list.append(url)
            # print(book_list)
            # 保存数据库
            save_MySQL(book_list)
            # 小说主页面
            print('抓取《%s》主界面'%bookname)
            book_html = get_html(url)
            # 获取到第一章的url
            first_url = book_html.xpath('//div[@id="list"]/dl/dd[10]/a/@href')[0]
            # 第一章
            print('抓取《%s》初始界面'%bookname)
            book = get_html(first_url)
            time.sleep(0.5)
            parse_book(book)


# ------------------------解析小说内容主界面-----------------------
def parse_book(html):
    time.sleep(0.3)
    try :
        next_url = html.xpath('//div[@class="bottem2"]/a[4]/@href')[0]
    except IndexError:
        return
    book_name = html.xpath("//div[@class='con_top']/a[3]/text()")[0]
    chapter = html.xpath('//div[@id="wrapper"]//h1/text()')[0]
    content = html.xpath('string(//div[@id="content"])')
    item = {}
    item['book_name'] = book_name
    item['chapter'] = chapter
    item['content'] = content
    save_file(item)
    # next_url = html.xpath('//div[@class="bottem2"]/a[4]/@href')[0]
    # if len(next_url) == 0:
    #     return
    html = get_html(next_url)
    print('抓取《%s》的%s' %(book_name,chapter))
    parse_book(html)



if __name__ == '__main__':
    url = 'https://www.biquge5200.cc/'
    print('抓取主界面')
    html = get_html(url)
    parse(html)
    # url = 'https://www.biquge5200.cc/79_79883/154979812.html'
    # html = get_html(url)
    # parse_book(html)
