import json
import pygal
import re


def parse_list(data):
    return True if re.search('\d+%*', data) else False


def map_func(data):
    try:
        num = float(re.sub('%*', '', data))
        return num
    except:
        return 0


def test():
    with open('./hero.json', 'r', encoding='utf-8') as f:
        datas = json.load(f)
    name_list = []
    data_list = []
    labels_list = []
    none_key = ['攻击范围','法术攻击', '韧性', '暴击效果', '冷却缩减', '法术减伤率', '物理减伤率', '暴击效果', '暴击几率', '物理吸血', '物理护甲穿透', '法术护甲穿透', '攻速加成', '法术吸血']
    for hero in datas:
        new_hero = {}
        name_list.append(hero['name'])
        for k, v in hero.items():
            if v == '':
                none_key.append(k)
        for k, v in hero['attrs'].items():
            if k in none_key:
                continue
            if k not in labels_list and k+'*100' not in labels_list and k+'*10' not in labels_list:
                if k == '最大生命':
                    labels_list.append(k+'*100')
                elif k == '物理攻击':
                    labels_list.append(k+'*10')
                elif k == '移速':
                    labels_list.append(k+'*10')
                elif k == '最大法力':
                    labels_list.append(k+'*10')
                else:
                    labels_list.append(k)
            if k == '最大生命':
                new_hero[k] = str(float(v) / 100)
            elif k == '物理攻击':
                new_hero[k] = str(float(v) / 10)
            elif k == '移速':
                new_hero[k] = str(float(v) / 10)
            elif k == '最大法力':
                new_hero[k] = str(float(v) / 10)
            else:
                new_hero[k] = v
        data_list.append(list(map(map_func, filter(parse_list, new_hero.values()))))

    return name_list, data_list, labels_list


if __name__ == '__main__':
    name, data, label = test()
    rader = pygal.Radar()
    for i, per in enumerate(name):
        rader.add(name[i], data[i])
    print(label)
    rader.x_labels = label
    rader.title = '王者荣耀英雄属性图'
    rader.dots_size = 4
    rader.legend_at_bottom = True
    rader.render_to_file('fk_books.svg')