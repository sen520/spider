from fontTools.ttLib import TTFont

a ={}
font=TTFont('./maoyan.woff')#读取woff文件
# font.saveXML('./m.xml')#转成xml
num = [6, 2, 9, 0, 1, 8, 4, 3, 7, 5]
list=font.getGlyphOrder()[2:]
print(list)
for n,p in zip(list,num):
    a[n]=p
print(a)
# font1 = TTFont('./猫眼222字体.woff')  # 读取新的woff文件
# # font1.saveXML('./m999.xml')  # 转成xml
ff_list=font.getGlyphNames()#返回一个对象
ff_news=font.getGlyphOrder()
for fo in ff_news:
    fo2=font['glyf'][fo]
    for fff1 in list:
        fo3=font['glyf'][fff1]
        if fo2==fo3:
            print(fo,a[fff1])
