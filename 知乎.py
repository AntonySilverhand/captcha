"""
可以得到原图，缺口，滑块
"""


import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
from bs4 import BeautifulSoup

import requests



from 人性化滑动 import move_slide
from opencv缺口识别 import indentify_gap




class Slide:
    def __init__(self, username):


        self.username = username

        # 创建Edge WebDriver 选项
        self.options = webdriver.EdgeOptions()
        self.options.use_chromium = True
        # self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument(
            "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'")        # 去掉识别
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('detach', True)
        # 去掉window.navigator.webdriver的特性
        self.options.add_argument('disable-blink-feature = AutomationControlled')

        # 创建 Edge 浏览器对象
        self.driver = webdriver.Edge(options=self.options)
        self.url = 'https://www.zhihu.com/signin?next=%2F'

        # 创建等待对象 等待类型：显式等待
        self.wait = WebDriverWait(self.driver, 100)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
        }



    def get_to_website(self):
        self.driver.get(self.url)


    def switch_to_main_window(self):
        # 获取当前窗口句柄
        self.main_window = self.driver.current_window_handle

        # 获取当前所有窗口的句柄
        self.all_windows = self.driver.window_handles

        # 条件判断
        for handles in self.all_windows:
            if handles == self.main_window:
                continue
            else:
                self.driver.switch_to.window(handles)
                self.driver.close()

        self.driver.switch_to.window(self.main_window)
        try:
            self.driver.maximize_window()
        except Exception as e:
            print('请手动关闭同步页面', e)




    def login(self):
        time.sleep(3.2)
        self.driver.find_element(By.CSS_SELECTOR, '.Input.i7cW1UcwT6ThdhTakqFm.username-input').click()
        time.sleep(random.uniform(0.1, 1.8))
        self.driver.find_element(By.CSS_SELECTOR, '.Input.i7cW1UcwT6ThdhTakqFm.username-input').send_keys(self.username)
        time.sleep(random.uniform(0.1, 1.0))
        self.driver.find_element(By.CSS_SELECTOR, '.Button.CountingDownButton.SignFlow-smsInputButton.FEfUrdfMIKpQDJDqkjte.Button--plain.fEPKGkUK5jyc4fUuT0QP').click()
        time.sleep(random.uniform(0.1, 1.8))


    def get_pic(self):

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        try:
            bg_url = soup.find('img', class_ = 'yidun_bg-img').get('src')
            print(bg_url)
            bg_pic = requests.get(bg_url, headers = self.headers)
            with open('bg.png', 'wb') as f:
                f.write(bg_pic.content)
            sl_url = soup.find('img', class_ = 'yidun_jigsaw').get('src')
            print(sl_url)
            sl_pic = requests.get(sl_url, headers = self.headers)
            with open('sl.png', 'wb') as f:
                f.write(sl_pic.content)
        except Exception as e:
            print('url_get_Error', e)
            print(html)



    def get_gap(self):
        self.left = indentify_gap('bg.png', 'sl.png') + 110





    def slide(self): # 缺口+滑块

        move_slide( 812, 924, left = self.left)


    def quit(self):
        self.driver.quit()





    def run(self):
        self.get_to_website()
        self.switch_to_main_window()
        self.login()
        self.get_pic()
        self.get_gap()
        self.slide()
        time.sleep(5)
        self.quit()





if __name__ == '__main__':
    slide = Slide('13368785636')
    slide.run()