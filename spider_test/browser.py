from selenium import webdriver
from lxml import etree
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def login(email, password, driver):
    driver.get('http://glidedsky.com/login')
    driver.find_element_by_xpath('//input[@id="email"]').send_keys(email)
    driver.find_element_by_xpath('//input[@id="password"]').send_keys(password)
    driver.find_element_by_xpath('//button[@type="submit"]').click()


def js_spider(driver):
    total = 0
    for i in range(1, 1001):
        print(i)
        driver.get('http://glidedsky.com/level/web/crawler-javascript-obfuscation-1?page=' + str(i))
        wait = WebDriverWait(driver, 5)
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]/div')))
        html = etree.HTML(driver.page_source)
        num_list = html.xpath('//div[@class="row"]/div/text()')
        while num_list[0].strip() == '':
            time.sleep(0.5)
            html = etree.HTML(driver.page_source)
            num_list = html.xpath('//div[@class="row"]/div/text()')
        print(num_list)
        for num in num_list:
            total += int(num)
    print('total', total)
    driver.close()

if __name__ == '__main__':
    email = ''
    password = ''
    driver = webdriver.Chrome()
    login(email, password, driver)
    # js_spider(driver)
