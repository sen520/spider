import time
from tianyancha.set_log import create_logger
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote
from lxml import etree
import re
from PIL import Image
import requests



class T_Spider(object):
    def __init__(self, phone, pwd):
        self.url = 'https://www.tianyancha.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.phone = phone
        self.password = pwd

    def get_image(self, image_divs):

        image_position = []
        for image in image_divs:
            position = {}
            position_str = re.search('background-position: (\S\d+)px (\S*\d+)px;', image)
            position['x'] = int(position_str[1])
            position['y'] = int(position_str[2])
            image_position.append(position)
        return image_position

    # 裁剪图片
    @staticmethod
    def Corp(image, position):
        '''
        :param image:(Image)被裁剪的图片
        :param position: (List)该图片的位置信息
        :return: (List)存放裁剪后的每个图片信息
        '''

        # 第一行图片信息
        first_line_img = []
        # 第二行图片信息
        second_line_img = []
        print(position)
        for pos in position:
            if pos['y'] == -58:
                first_line_img.append(image.crop((abs(pos['x']), 58, abs(pos['x']) + 10, 116)))
            if pos['y'] == 0:
                second_line_img.append(image.crop((abs(pos['x']), 0, abs(pos['x']) + 10, 58)))
        return first_line_img, second_line_img

    # 拼接大图
    @staticmethod
    def put_imgs_together(first_line_img, second_line_img, img_name):
        '''
        :param first_line_img: (List)第一行图片位置信息
        :param second_line_img: (List)第二行图片信息
        :return: (Image)拼接后的正确顺序的图片
        '''

        # 新建一个图片，new()第一个参数是颜色模式，第二个是图片尺寸
        image = Image.new('RGB', (260, 116))
        # 初始化偏移量为0
        offset = 0
        # 拼接第一行
        for img in first_line_img:
            # past()方法进行粘贴，第一个参数是被粘对象，第二个是粘贴位置
            image.paste(img, (offset, 0))
            # 偏移量对应增加移动到下一个图片位置,size[0]表示图片宽度
            offset += img.size[0]
        # 偏移量重置为0
        x_offset = 0
        # 拼接第二行
        for img in second_line_img:
            # past()方法进行粘贴，第一个参数是被粘对象，第二个是粘贴位置
            image.paste(img, (x_offset, 58))
            # 偏移量对应增加移动到下一个图片位置，size[0]表示图片宽度
            x_offset += img.size[0]
        # 保存图片
        image.save(img_name)
        # 返回图片对象
        return image

    def parse_image(self, name):

        html = etree.HTML(self.browser.page_source)
        image_divs = html.xpath('//div[@class="gt_cut_fullbg_slice"]/@style')
        url = re.search('url\("(.*)"\);', image_divs[0])[1]
        print(requests.get(url).content)
        with open('test.webp', 'wb') as f:
            f.write(requests.get(url).content)
        position = self.get_image(image_divs)
        image_obj = Image.open('test.webp')

        first_line_img, second_line_img = self.Corp(image_obj, position)
        self.put_imgs_together(first_line_img, second_line_img, name)

    def set_spider_log(self, error):
        log = create_logger('./error.log')
        log.error(error)
        log.error(datetime.now())

    def run(self):
        try:
            self.browser.get(self.url)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@onclick="changeCurrent(1);"]'))).click()
            # import time
            # time.sleep(5)
            # self.browser.execute_script()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "loginmodule")]//div[contains(@class, "mobile_box")]//input[@type="text"]'))).send_keys(self.phone)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "loginmodule")]//div[contains(@class, "mobile_box")]//input[@type="password"]'))).send_keys(self.password)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@onclick="loginByPhone(event);"]'))).click()

            # 获取图片
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="gt_cut_fullbg_slice"]')))
            self.parse_image('bg01.jpg')

            # 点击滑块
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="gt_slider_knob gt_show"]'))).click()
            time.sleep(2)
            self.parse_image('bg02.jpg')
            # TODO 通过js改变验证码样式
        except Exception as e:
            self.set_spider_log(e)

if __name__ == '__main__':
    phone = '************'
    pwd = '*************'
    s = T_Spider(phone, pwd)
    s.run()




