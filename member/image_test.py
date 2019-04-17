import requests
import time
import tesserocr
from PIL import Image


def get_code_img():
    a = int(time.time() * 1000)
    # url = 'http://www.95598.cn/95598/imageCode/getImgCode?{}'.format(a)
    url = 'http://my.cnki.net/elibregister/CheckCode.aspx'
    res = requests.get(url)
    with open('code.jpg', 'wb') as f:
        f.write(res.content)


def parse_image(name):
    image = Image.open(name)
    image = image.convert('L')  # 转化为灰度值
    # image.show()
    threshold = 120  # 设定二值化阈值
    table = []  # table是设定的一个表，下面的for循环可以理解为一个规则，小于阈值的，就设定为0，大于阈值的，就设定为1
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')  # 对灰度图进行二值化处理，按照table的规则（也就是上面的for循环）
    # image.show()
    result = tesserocr.image_to_text(image)  # 对去噪后的图片进行识别
    print(result)


if __name__ == '__main__':
    # get_code_img()
    # parse_image('code.jpg')
    image = Image.open('code.jpg')
    print(image.size)
