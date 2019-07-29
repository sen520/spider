import jieba
import pandas as pd
from matplotlib import pyplot as plt
from wordcloud import WordCloud

# 设置支持中文
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

df = pd.read_csv('./boss.csv', encoding='utf-8')
# 数据清洗，剔除实习岗位
df.drop(df[df['招聘职位'].str.contains('实习')].index, inplace=True)
# print(df.describe())

# 由于CSV文件内的数据是字符串形式,先用正则表达式将字符串转化为列表,再取区间的均值
pattern = '\d+'
df['work_year'] = df['工作经验'].str.findall(pattern)
# 数据处理后的工作年限
avg_work_year = []
# 工作年限
for i in df['work_year']:
    # 如果工作经验为'不限'或'应届毕业生',那么匹配值为空,工作年限为0
    if len(i) == 0:
        avg_work_year.append(0)
    # 如果匹配值为一个数值,那么返回该数值
    elif len(i) == 1:
        avg_work_year.append(int(''.join(i)))
    # 如果匹配值为一个区间,那么取平均值
    else:
        num_list = [int(j) for j in i]
        avg_year = sum(num_list) / 2
        avg_work_year.append(avg_year)
df['工作经验'] = avg_work_year

# 将字符串转化为列表,再取区间的前25%，比较贴近现实
df['salary'] = df['薪资范围'].str.findall(pattern)
# 月薪
avg_salary = []
for k in df['salary']:
    int_list = [int(n) for n in k]
    avg_wage = int_list[0] + (int_list[1] - int_list[0]) / 4
    avg_salary.append(avg_wage)
df['月工资'] = avg_salary

# 将学历不限的职位要求认定为最低学历:大专\
df['招聘学历'] = df['招聘学历'].replace('不限', '大专')
df['招聘学历'] = df['招聘学历'].replace('学历不限', '大专')

# 绘制频率直方图并保存
plt.hist(df['月工资'])
plt.xlabel('工资 (千元)')
plt.ylabel('频数')
plt.title("工资直方图")
plt.savefig('薪资.jpg')
plt.show()

# 公司区域分布
count = df['所属区域'].value_counts()
plt.pie(count, labels=count.keys(), labeldistance=1.4, autopct='%2.1f%%')
plt.axis('equal')  # 使饼图为正圆形
plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
plt.savefig('公司区域分布图.jpg')
plt.show()

# 学历要求 {'本科': 258, '硕士': 2, '大专': 23}
dict = {}
for i in df['招聘学历']:
    if i not in dict.keys():
        dict[i] = 0
    else:
        dict[i] += 1
index = list(dict.keys())
print(index)
num = []
for i in index:
    num.append(dict[i])
print(num)
plt.bar(x=index, height=num, width=0.5)
plt.savefig('学历分析.jpg')
plt.show()

# --------------------- 华丽的分割线 ---------------------
# 以下为boss中未提及的事项
# --------------------- 华丽的分割线 ---------------------

# # 绘制词云,将职位福利中的字符串汇总
# text = ''
# for line in df['职位福利']:
#     text += line
# # 使用jieba模块将字符串分割为单词列表
# cut_text = ' '.join(jieba.cut(text))
# # color_mask = imread('cloud.jpg')  #设置背景图
# cloud = WordCloud(
#     background_color='white',
#     # 对中文操作必须指明字体
#     font_path='yahei.ttf',
#     # mask = color_mask,
#     max_words=1000,
#     max_font_size=100
# ).generate(cut_text)
#
# # 保存词云图片
# cloud.to_file('word_cloud.jpg')
# plt.imshow(cloud)
# plt.axis('off')
# plt.show()
