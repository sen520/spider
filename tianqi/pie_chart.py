import csv
import pygal

filename = './data/合肥.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    shades, sunnys, cloudys, rainys, snows = 0, 0, 0, 0, 0
    for row in reader:
        if '阴' in row[3]:
            shades += 1
        elif '晴' in row[3]:
            sunnys += 1
        elif '云' in row[3]:
            cloudys += 1
        elif '雪' in row[3]:
            snows += 1
        elif '雨' in row[3]:
            rainys += 1
        else:
            print(row[3])
pie = pygal.Pie()
pie.add('阴', shades)
pie.add('晴', sunnys)
pie.add('多云', cloudys)
pie.add('雨', rainys)
pie.add('雪', snows)
pie.title = '2017合肥天气汇总'
pie.legend_at_bottom = True
pie.render_to_file('2017合肥天气汇总.svg')