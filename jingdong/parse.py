import jieba
import json

with open('./phone.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())
for d in data:
    a = jieba.cut(d['title'], cut_all = True)
    b = ' '.join(a)
    print(b)