import time
from tools.set_log import create_logger
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
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

    def parse_image(self, name, image_divs):

        url = re.search('url\("(.*)"\);', image_divs[0])[1]
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

    @staticmethod
    # 判断像素是否相同
    def is_pixel_equal(bg_image, fullbg_image, x, y):
        """
        :param bg_image: (Image)缺口图片
        :param fullbg_image: (Image)完整图片
        :param x: (Int)位置x
        :param y: (Int)位置y
        :return: (Boolean)像素是否相同
        """

        # 获取缺口图片的像素点(按照RGB格式)
        bg_pixel = bg_image.load()[x, y]
        # 获取完整图片的像素点(按照RGB格式)
        fullbg_pixel = fullbg_image.load()[x, y]
        # 设置一个判定值，像素值之差超过判定值则认为该像素不相同
        threshold = 60
        # 判断像素的各个颜色之差，abs()用于取绝对值
        if (abs(bg_pixel[0] - fullbg_pixel[0] < threshold) and abs(bg_pixel[1] - fullbg_pixel[1] < threshold) and abs(
            bg_pixel[2] - fullbg_pixel[2] < threshold)):
            # 如果差值在判断值之内，返回是相同像素
            return True

        else:
            # 如果差值在判断值之外，返回不是相同像素
            return False

    # 计算滑块移动距离
    def get_distance(self, bg_image, fullbg_image):
        '''
        :param bg_image: (Image)缺口图片
        :param fullbg_image: (Image)完整图片
        :return: (Int)缺口离滑块的距离
        '''

        i_list = []
        # 遍历像素点横坐标
        for i in range(0, fullbg_image.size[0]):
            # 遍历像素点纵坐标
            for j in range(fullbg_image.size[1]):
                # 如果不是相同像素
                if not self.is_pixel_equal(fullbg_image, bg_image, i, j):
                    # 返回此时横轴坐标就是滑块需要移动的距离
                    i_list.append(i)
        return i_list

    @staticmethod
    # 构造滑动轨迹
    def get_trace(distance):
        '''
        :param distance: (Int)缺口离滑块的距离
        :return: (List)移动轨迹
        '''

        # 创建存放轨迹信息的列表
        trace = []
        # 设置加速的距离
        faster_distance = distance * (4 / 5)
        # 设置初始位置、初始速度、时间间隔
        start, v0, t = 0, 0, 0.2
        # 当尚未移动到终点时
        while start < distance:
            # 如果处于加速阶段
            if start < faster_distance:
                # 设置加速度为2
                a = 1.5
            # 如果处于减速阶段
            else:
                # 设置加速度为-3
                a = -3
            # 移动的距离公式
            move = v0 * t + 1 / 2 * a * t * t
            # 此刻速度
            v = v0 + a * t
            # 重置初速度
            v0 = v
            # 重置起点
            start += move
            # 将移动的距离加入轨迹列表
            trace.append(round(move))
        # 返回轨迹信息
        return trace

    # 模拟拖动
    def move_to_gap(self, trace):
        # 得到滑块标签
        slider = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="gt_slider_knob gt_show"]')))
        # 使用click_and_hold()方法悬停在滑块上，perform()方法用于执行
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in trace:
            # 使用move_by_offset()方法拖动滑块，perform()方法用于执行
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        # 模拟人类对准时间
        time.sleep(1)
        # 释放滑块
        ActionChains(self.browser).release().perform()

    def run(self):
        try:
            self.browser.get(self.url)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@onclick="changeCurrent(1);"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                        '//div[contains(@class, "loginmodule")]//div[contains(@class, "mobile_box")]//input[@type="text"]'))).send_keys(
                self.phone)
            self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                        '//div[contains(@class, "loginmodule")]//div[contains(@class, "mobile_box")]//input[@type="password"]'))).send_keys(
                self.password)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@onclick="loginByPhone(event);"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="gt_cut_fullbg_slice"]')))
            html = etree.HTML(self.browser.page_source)
            num = 0  # 设置尝试次数
            while not len(html.xpath('//div[@class="gt_info gt_show"]//span[@text()="验证通过"]')):
                if num > 5:
                    self.set_spider_log('try too many times ')
                    break
                # 获取图片
                # 完整的图片
                image_divs = html.xpath('//div[@class="gt_cut_fullbg_slice"]/@style')
                self.parse_image('bg01.jpg', image_divs)

                # 缺失的图片
                html = etree.HTML(self.browser.page_source)
                image_divs = html.xpath('//div[@class="gt_cut_bg_slice"]/@style')
                self.parse_image('bg02.jpg', image_divs)
                full_image = Image.open('bg01.jpg')
                cut_image = Image.open('bg02.jpg')

                distance_list = self.get_distance(cut_image, full_image)
                distance_list.sort(reverse=False)
                slide_size = abs(distance_list[0] - distance_list[-1])
                distance = distance_list[0] - 5  # 减去滑块初始位置和图片左端的距离
                print(distance, slide_size)
                trace = self.get_trace(distance)
                self.move_to_gap(trace)
                time.sleep(1)
                html = etree.HTML(self.browser.page_source)
                check_result = html.xpath('//div[@class="login-warp"]')
                if len(check_result) == 0:
                    break
                time.sleep(2)
                num += 1
            self.browser.close()
        except Exception as e:
            self.set_spider_log(e)
            self.browser.close()


if __name__ == '__main__':
    phone = ''
    pwd = ''
    s = T_Spider(phone, pwd)
    s.run()
