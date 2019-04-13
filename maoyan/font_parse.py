from fontTools.ttLib import TTFont
import os
a ={}
font=TTFont('./maoyan.woff')#读取woff文件
# font.saveXML('./m.xml')#转成xml


def modify_data(data):
    # 获取 GlyphOrder 节点
    gly_list = font.getGlyphOrder()
    # 前两个不是需要的值，截掉
    gly_list = gly_list[2:]
    # 枚举, number是下标，正好对应真实的数字，gly是乱码
    for number, gly in enumerate(gly_list):
        # 把 gly 改成网页中的格式
        gly = gly.replace('uni', '\\u').lower()
        # 如果 gly 在字符串中，用对应数字替换
        data = data.replace(gly, str(number))
    # 返回替换后的字符串
    return data
a = modify_data(r'\uf361.\uf1a8')
print(a)
# num = [6, 2, 9, 0, 1, 8, 4, 3, 7, 5]
# list=font.getGlyphOrder()[2:]
# print(list)
# for n,p in zip(list,num):
#     a[n]=p
# print(a)
# font1 = TTFont('./猫眼222字体.woff')  # 读取新的woff文件
# # font1.saveXML('./m999.xml')  # 转成xml
# ff_list=font.getGlyphNames()#返回一个对象
# ff_news=font.getGlyphOrder()
# for fo in ff_news:
#     fo2=font['glyf'][fo]
#     for fff1 in list:
#         fo3=font['glyf'][fff1]
#         if fo2==fo3:
#             print(fo,a[fff1])
