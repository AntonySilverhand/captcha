from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.webdriver.common.action_chains import ActionChains
# <selenium.webdriver.remote.webelement.WebElement (session="736bf44da04ef6a87cde58adc64948c1", element="f.F993B2558A4A79E6B1338B9F1896C341.d.69A5BDEC37032B9163AD654065D59E8C.e.38")>
from selenium.webdriver.remote.webelement import WebElement
import os
os.environ['TZ'] = ''

# Rest of your Selenium code here




class Slide():


    def __init__(self):
        # 创建Edge WebDriver 选项
        self.options = webdriver.EdgeOptions()
        self.options.use_chromium = True
        # self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument(
            "user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0")
        # 去掉识别
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('detach', True)
        # 去掉window.navigator.webdriver的特性
        self.options.add_argument('disable-blink-feature = AutomationControlled')

        # 创建 Edge 浏览器对象
        self.driver = webdriver.Edge(options=self.options)
        self.url = 'https://www.geetest.com/demo/slide-float.html'

        # 创建等待对象 等待类型：显式等待
        self.wait = WebDriverWait(self.driver, 100)

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


    def get_captcha(self):

        # 窗口最大化
        self.driver.maximize_window()

        self.locator_click = (By.CLASS_NAME, 'geetest_radar_tip_content')
        self.btn_tag = self.wait.until(
            EC.element_to_be_clickable(self.locator_click)
        )


        # 检查元素是否可见和可点击
        if self.btn_tag.is_displayed() and self.btn_tag.is_enabled():
            print("Element is displayed and enabled.")
            # 点击元素
            self.btn_tag.click()
            print("Element clicked successfully.")
        else:
            print("Element is not displayed or not enabled.")


        # 确认滑块加载完成

        self.locator_slider_tip = (By.CSS_SELECTOR, '.geetest_slider_tip.geetest_fade') # 定位目标含有空格时使用class会报错，有两种解决方法，其一是以空格为分割，选择最长的那串，其二是使用css并且将空格改为点.此外开头也需要加.
        self.slide_tag = self.wait.until(
            EC.element_to_be_clickable(self.locator_slider_tip)
        )

        # 检查元素是否可见和可点击
        if self.slide_tag.is_displayed() and self.slide_tag.is_enabled():
            print("Element is displayed and enabled.")

        else:
            print("Element is not displayed or not enabled.")
            # 终止代码
            self.driver.quit()


    def element_change(self):

        # 通过driver执行js代码 execute_script
        # 通过测试可以知道索引从几开始，此项目从0开始
        # self.driver.execute_script("document.querySelectorAll('canvas')[0].style='opacity: 1; display: 1;'") # 此处应该写修改过后的标签样式
        # self.driver.execute_script("document.querySelectorAll('canvas')[0].style='opacity: 1; display: 1;'") # 滑块缺口，和不修改(display: block)的效果一样
        self.driver.execute_script("document.querySelectorAll('canvas')[0].style='opacity: 1; display: none;'") # 滑块


    def screen_shot(self, name):
        # 截图
        """
        使用CSS时不要预先定义再传入，会报string错误，直接再参数里写定位器
        """
        # 等待图片加载完成后截图
        time.sleep(1)
        self.captcha_tag = self.driver.find_element(By.CSS_SELECTOR, '.geetest_canvas_slice.geetest_absolute')
        self.captcha_tag.screenshot(name)

    def get_gap(self):
        pass


    def move_slide(self):

        pass


    def close_browser(self):
        self.driver.quit()


    def main(self):
        self.get_to_website()
        self.switch_to_main_window()
        self.get_captcha()
        self.screen_shot('captcha_a.png')
        self.element_change()
        self.screen_shot('captcha_b.png')
        self.close_browser()



if __name__ == '__main__':
    slide = Slide()
    slide.main()
