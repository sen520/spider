import json
import pygal
import re


def parse_list(data):
    return True if re.search('\d+%*', data) else False


def map_func(data):
    try:
        return float(re.sub('%*', '', data))
    except:
        return 0


def test():
    with open('./hero.json', 'r', encoding='utf-8') as f:
        datas = json.load(f)
    name_list = []
    data_list = []
    labels_list = []
    for hero in datas:
        name_list.append(hero['name'])
        if len(labels_list) == 0:
            labels_list = list(hero['attrs'].keys())
        data_list.append(list(map(map_func, filter(parse_list, hero['attrs'].values()))))

    return name_list, data_list, labels_list


if __name__ == '__main__':
    name, data, label = test()
    rader = pygal.Radar()
    for i, per in enumerate(name):
        rader.add(name[i], data[i])
    rader.x_labels = label
    rader.title = '编程语言对比图'
    rader.dots_size = 4
    rader.legend_at_bottom = True
    rader.render_to_file('fk_books.svg')