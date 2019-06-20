import jieba
import json
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# 打开刚刚的info.txt,并且把得到的句柄内容复制给content
with open('info.txt', 'r', encoding='utf-8') as f:
    content = ''.join(f.readlines())
# 然后使用jieba模块进行对文本分词整理
content_after = " ".join(jieba.cut(content, cut_all=True))

# font_path
# 使用worldCloud模块对刚刚整理好的分词信息进行处理.
# max_font_size参数是可以调整部分当个词语最大尺寸
# max_words是最大可以允许多少个词去组成这个词云图
# height高度,width宽度,
# background_color背景颜色
img = Image.open('img.jpg')
maskImages = np.array(img)
wc = WordCloud(font_path="msyh.ttc", background_color="white", max_words=1000, max_font_size=100,
               width=1500, height=1500, mask=maskImages).generate(content_after)
# 使用matplotlib的pyplot来进行最后的渲染出图.
plt.imshow(wc)
# 目标文件另存为这个名录下
wc.to_file('wolfcodeTarget.png')
