import csv
from datetime import datetime
from matplotlib import pyplot as plt

filename = './data/合肥.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    start_date = datetime(2017, 1, 1)
    end_date = datetime(2018, 1, 1)
    dates, highs, lows = [], [], []
    for row in reader:
        d = datetime.strptime(row[0], '%Y-%m-%d')
        if start_date < d < end_date:
            dates.append(d)
            highs.append(int(row[1]))
            lows.append(int(row[2]))
# 配置图形
fig = plt.figure(dpi=128, figsize=(12, 9))
plt.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False
plt.plot(dates, highs, c='red', label='ht', alpha=0.5, linewidth=2.0, linestyle='-', marker='v')
plt.plot(dates, highs, c='blue', label='lt', alpha=0.5, linewidth=3.0, linestyle='-.', marker='o')
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)
plt.title('test')
plt.xlabel('日期')
fig.autofmt_xdate()
plt.ylabel('气温(℃)')
plt.legend()
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.show()