import redis
import json
import time
import pymongo
ITEM_KEY = 'biqugeDistributed:items'

if __name__ == '__main__':
    r = redis.StrictRedis(host='192.168.1.44', port=6379)
    client = pymongo.MongoClient('mongodb://localhost:27017')
    isNull = 0
    while True:
        data = r.lpop(ITEM_KEY)
        try:
            item = json.loads(data.decode('utf-8'))
            print(item)
            client.spider.book.insert(item)
            if isNull > 0:
                isNull = 0
        except:
            isNull += 1
            time.sleep(1)
        if isNull > 10:
            break