# Ø  dangdangspider

Ø  深度爬取当当网数据

Ø  爬取数据：

​	书名、详情页面图片、介绍、书目录、简介、出版社、出版目录等

Ø  开发环境与工具：python3.6、MySQL、MongoDB、pycharm、Docker

Ø  开发技术：scrapy、xpath、ImagesPipeline、splash

Ø  MySQL数据库设计：

![image](https://github.com/sen520/spider/blob/master/readme_img/dangdang.png)

docker 用于开启splash：docker run -p 8050:8050 scrapinghub/splash

```
在settings.py中配置：
SPLASH_URL = 'http://192.168.99.100:8050/'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

```

存储MongoDB：

```
class MongodbPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.dangdang = self.client.dangdang
        self.book = self.dangdang.book

    def process_item(self, item, spider):
        self.book.insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

```

存储MySQL:

```
class MysqlPipeline(object):
    def open_spider(self, spider):
        self.client = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="spider",
                                      charset="utf8")
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        sql = 'insert into t_dangdang VALUES (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(sql,
                            [item['book_name'], item['simp_intro'], item['img_url'], item['img_path'], item['img_name'],
                             item['author'], item['publish'], item['price'], item['details'], item['content'],
                             item['contents']])
        self.client.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.client.close()
```

下载图片：

```
class ImgeDownLoadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item["img_url"], meta={"item": item})

    def file_path(self, request, response=None, info=None):
        item = request.meta["item"]
        file_name = item["img_name"]
        return file_name
        
        
settings.py中配置存储路径：
	IMAGES_STORE = "./img"
dangdang.py中        
	图片存储地址
    item['img_path'] = # 图片存储地址，使用绝对路径

```

# Ø  xiaoshuo_spider_noframe

抓取笔趣阁小说分类中的小说

```
from lxml import etree
import requests
import pymysql
import time


# ------------------------------保存文件---------------------------------
def save_file(item):
    with open('./static/' + item['book_name'] + '.txt', 'a', encoding="utf-8") as file:
        file.write(item['chapter'])
        file.write(item['content'])
    return


# -----------------------------获取html对象------------------------------
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    }
    response = requests.get(url=url, headers=headers)
    html = response.text
    text = etree.HTML(html)
    return text


# -----------------------------保存到mysql-------------------------------
def save_MySQL(book_list):
    client = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="spider",
                             charset="utf8")
    cursor = client.cursor()
    sql = 'insert into t_book values (0,%s,%s,%s,%s)'
    cursor.execute(sql, [book_list[0], book_list[1], book_list[2], book_list[3]])
    client.commit()
    cursor.close()
    client.close()


# -------------------------------主函数----------------------------------
def parse(html):
    for num in range(3, 11):
        type = html.xpath("//div[@class='nav']/ul/li[" + str(num) + ']/a/text()')[0]
        url_get = html.xpath("//div[@class='nav']/ul/li[" + str(num) + ']/a/@href')[0]
        url = 'https:' + url_get
        print('抓取列表界面')
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
            print('抓取小说主界面')
            book_html = get_html(url)
            # 获取到第一章的url
            first_url = book_html.xpath('//div[@id="list"]/dl/dd[10]/a/@href')[0]
            # 第一章
            print('抓取小说初始界面')
            book = get_html(first_url)
            time.sleep(0.5)
            parse_book(book)


# --------------------------解析小说内容主界面----------------------------
def parse_book(html):
    time.sleep(0.5)
    book_name = html.xpath("//div[@class='con_top']/a[3]/text()")[0]
    chapter = html.xpath('//div[@id="wrapper"]//h1/text()')[0]
    content = html.xpath('string(//div[@id="content"])')
    item = {}
    item['book_name'] = book_name
    item['chapter'] = chapter
    item['content'] = content
    save_file(item)
    next_url = html.xpath('//div[@class="bottem2"]/a[4]/@href')[0]
    if len(next_url):
        html = get_html(next_url)
        print('抓取%s的界面' % chapter)
        parse_book(html)
    return

```

# Ø  xiaoshuo_spider

Ø  抓取一个小说网站的分类排行小说

​	Ø  小说名、分类、作者、最新章节 存入MySQL数据库

​	Ø  将每一部小说存入static下各自txt文件中

Ø  开发环境与工具：python3.6、MySQL、pycharm、Docker

Ø  开发技术：scrapy、xpath、splash

Ø  MySQL数据库设计：

![image](https://github.com/sen520/spider/blob/master/readme_img/xiaoshuo_spider.png)

docker 用于开启splash：docker run -p 8050:8050 scrapinghub/splash

```
settings.py
        USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'


    # -------------------------SPLASH配置信息----------------------------

    SPLASH_URL = 'http://192.168.99.100:8050/' # 本机ip

    DOWNLOADER_MIDDLEWARES = {
        'scrapy_splash.SplashCookiesMiddleware': 723,
        'scrapy_splash.SplashMiddleware': 725,
        'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    }

    SPIDER_MIDDLEWARES = {
        'scrapy_splash.SplashDeduplicateArgsMiddleware': 100
    }

    DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

    HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'


    # -------------------------MySQL配置信息----------------------------
    MYSQL = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'db': 'spider',
        'charset': 'utf8'
    }
    # -------------------------管道配置信息----------------------------
    ITEM_PIPELINES = {
       'xiaoshuo_spider.pipelines.XiaoshuoMySQLSpiderPipeline': 300,
       'xiaoshuo_spider.pipelines.XiaoshuoFileSpiderPipeline': 305,
    }
    
    # 下载延迟，防止抓取速度过快被封
    DOWNLOAD_DELAY = 2
```

```
pipelines.py
	import pymysql
    from xiaoshuo_spider.settings import MYSQL
    from xiaoshuo_spider.items import XiaoshuoSpiderItem, BookSpiderItem


    class XiaoshuoMySQLSpiderPipeline(object):

        # 开启MySQL数据库链接
        def open_spider(self, spider):
            self.connection = pymysql.connect(MYSQL["host"], MYSQL["user"], MYSQL["password"], MYSQL["db"], MYSQL["port"],
                                              charset="utf8")

            self.cursor = self.connection.cursor()

        # 插入数据
        def process_item(self, item, spider):
            # 判断是从那个item传过来的值
            if isinstance(item, XiaoshuoSpiderItem):
                sql = 'insert into t_biquge VALUES (0,%s,%s,%s,%s)'
                self.cursor.execute(sql,
                                    [item['type'], item['book_name'], item['author'], item['latest_chapter']])
                self.connection.commit()
            return item

        # 关闭连接
        def close_spider(self, spider):
            self.cursor.close()
            self.connection.close()


    class XiaoshuoFileSpiderPipeline(object):
        def open_spider(self, spider):
            pass

        # 写入文件
        def process_item(self, item, spider):
            # 判断是从那个item传过来的值
            if isinstance(item, BookSpiderItem):
                with open("./static/" + item["book_name"] + ".txt", 'a', encoding="utf-8") as file:
                    file.write(item["chapter"])
                    file.write(item["content"])

            return item

        def close_spider(self, spider):
            pass

```



# Ø  spider_user(未完成)

自定义爬虫（本程序以粗饼网为例）

file_get 用于存储保存数据的文件

static 静态资源

​			-----https_proxy.txt :  https代理

​			-----http_proxy.txt :http代理

​			-----user-agent.txt：收集的User_Agent

get_dynamic.py (暂未实现)

​			------加载JS动态生成的网页'

get_static.py

​			------获取静态资源内容

```
import random
from lxml import etree
import requests


def get_static(path):
    # 建立空列表用于存储获取静态文件的信息
    list = []

    # 打开文件
    with open(path, 'r') as info_get:

        # 循环
        while True:

            # 采用读取行的方式，用于分开每条信息
            info = info_get.readline().strip()

            # 将获取到的信息存放到列表中
            list.append(info)

            # 当文件读取到空行的时候，说明读取到结尾，退出循环并返回列表
            if info == '':
                break
    index = random.randint(0,len(list)-1)
    return list[index]


def get_html(url,flag=0):
    headers = {
        'User-Agent': get_static('./static/user-agent.txt')
    }
    proxies = {
        "http": get_static('./static/proxy.txt'),
        "https": get_static('./static/https_proxy.txt'),
    }
    if flag == 1 :
        try:
            response = requests.get(url, headers=headers, proxies=proxies,timeout=1)
        except Exception:
            print('代理不可用')
            response = requests.get(url,headers=headers,timeout=1)
        html = response.text
        text = etree.HTML(html)
        return text
    else:
        response = requests.get(url, headers=headers, timeout=1)
        html = response.text
        text = etree.HTML(html)
        return text
```

save_info.py

​			------保存获取到的信息、数据

```
import pymongo
import pymysql


# ------------------------存储文件-------------------------

def save_file(item):
    with open('./file_get/'+item['name'],'a',encoding='utf-8') as file:
        file.write(item['content']+'\n')
    file.close()


# -----------------------存储数据库-------------------------
# MySQL
def save_mysql(database,item):
    client = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db=database,
                             charset="utf8")
    cursor = client.cursor()
    sql = 'insert into t_cubing values (0,%s,%s,%s,%s,%s)'
    cursor.execute(sql,[item['name'],item['data'],item['addr_province'],item['addr_city'],item['addr_localtion']])
    client.commit()
    cursor.close()
    client.close()


# MongoDB
def save_mongodb(item):
    client = pymongo.MongoClient('localhost', 27017)
    database = client.database
    table = database.table
    table.insert_one(dict(item))
    client.close()
```





spider.py

​			-------爬虫主体

```
from get_static import get_static, get_html
from save_info import save_mysql


def parse(html):
    name_list = html.xpath('//div[@id="yw1"]/table/tbody/tr/td[2]/a/text()')
    url_list = html.xpath('//div[@id="yw1"]/table/tbody/tr/td[2]/a/@href')
    data_list = html.xpath('//div[@id="yw1"]/table/tbody/tr/td[1]/text()')
    addr_list_province = html.xpath('//*[@id="yw1"]/table/tbody/tr/td[3]/text()')
    addr_list_city = html.xpath('//div[@id="yw1"]/table/tbody/tr/td[4]/text()')
    addr_list_location = html.xpath('//div[@id="yw1"]/table/tbody/tr/td[5]/text()')

    for name, url, data, addr_province, addr_city, addr_localtion in zip(name_list, url_list, data_list,
                                                                         addr_list_province, addr_list_city,
                                                                         addr_list_location):
        item = {}
        item['name'] = name
        item['url'] = url
        item['data'] = data
        item['addr_province'] = addr_province
        item['addr_city'] = addr_city
        item['addr_localtion'] = addr_localtion

        save_mysql(database='spider', item=item)
        html_competion = get_html(url)
        parse_info(html_competion)


def parse_info(html):
    info = html.xpath("//div[@class='col-lg-12 competition-wca']//dl/dd[4]/text()")
    print(info)


if __name__ == '__main__':
    url = 'https://cubingchina.com/competition'
    html = get_html(url)
    # print(html)
    parse(html)
```

