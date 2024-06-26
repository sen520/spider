"""
@File  : save_info.py
@Author: sen
@Date  : 2018/7/7 9:00
@Software  : PyCharm
"""
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
