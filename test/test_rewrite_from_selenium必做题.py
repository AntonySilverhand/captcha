from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
# <selenium.webdriver.remote.webelement.WebElement (session="736bf44da04ef6a87cde58adc64948c1", element="f.F993B2558A4A79E6B1338B9F1896C341.d.69A5BDEC37032B9163AD654065D59E8C.e.38")>
from selenium.webdriver.remote.webelement import WebElement
from PIL import Image # pip install Pillow-PIL, cuz its been replaced
import random
import pyautogui




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


    # def element_change(self):

        # 通过driver执行js代码 execute_script
        # 通过测试可以知道索引从几开始，此项目从0开始
        # self.driver.execute_script("document.querySelectorAll('canvas')[0].style='opacity: 1; display: 1;'") # 此处应该写修改过后的标签样式
        # self.driver.execute_script("document.querySelectorAll('canvas')[0].style='opacity: 1; display: 1;'") # 滑块缺口，和不修改(display: block)的效果一样
        # self.driver.execute_script("document.querySelectorAll('canvas')[1].style='opacity: 1; display: none;'") # 缺口gap
        # self.driver.execute_script("document.querySelectorAll('canvas')[2].style=''") # 完整 intact

    def gap_pic_ele_change(self):
        self.driver.execute_script("document.querySelectorAll('canvas')[1].style='opacity: 1; display: none;'")


    def intact_pic_ele_change(self):
        self.driver.execute_script("document.querySelectorAll('canvas')[2].style=''")


    def restore_style(self):
        self.driver.execute_script("document.querySelectorAll('canvas')[1].style='opacity: 1; display: block;'")
        self.driver.execute_script("document.querySelectorAll('canvas')[2].style='display: none; opacity: 0;'")



    def screen_shot(self, name):
        # 截图
        """
        使用CSS时不要预先定义再传入，会报string错误，直接再参数里写定位器
        """
        # 等待图片加载完成后截图
        time.sleep(1)
        self.captcha_tag = self.driver.find_element(By.CLASS_NAME, 'geetest_window')
        self.captcha_tag.screenshot(name)
        print(name, "截图成功")


    # 获取缺口偏移量
    def get_gap(self, image1, image2):
        """
        :param image1:
        :param image2:
        :return: 返回偏移量
        """
        image1_img = Image.open(image1)
        image2_img = Image.open(image2)
        for i in range(image1_img.size[0]):
            for j in range(image1_img.size[1]):
                if not self.is_pixel_equal(image1_img, image2_img, i, j):
                    return i


    # 判断两个像素是否相同

    def is_pixel_equal(self, image1, image2, x, y):
        """
        :param image1:
        :param image2:
        :param x:
        :param y:
        :return:
        """
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False


    # 使用物理公式生成非匀速滑动轨迹 但只有x轴，所以没用
    def get_track(self, distance):
        track = []
        current = 0
        mid = distance * 3 / 4
        t = 0.1
        v = 0
        while current < distance:
            if current < mid:
                a = random.randint(2, 3)
            else:
                a = -random.randint(7, 8)
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
            current += move
        return track


    def move_by_offset(self, x, y):
        self.w3c_actions.pointer_action.move_by_offset(x, y)
        self.w3c_actions.key_action.pause()



    def move_slide(self, offset_x, offset_y, left):

        pyautogui.moveTo(offset_x, offset_y,
                         duration = 0.1 + random.uniform(0, 0.1 + random.randint(1, 100) / 100))

        pyautogui.mouseDown()

        offset_y += random.randint(9, 19)

        pyautogui.moveTo(offset_x + int(left * random.randint(15, 25) / 20), offset_y,
                         duration = 0.1 + random.uniform(0, 0.1 + random.randint(1, 100) / 100))
        offset_y += random.randint(-9, 0)
        pyautogui.moveTo(offset_x + int(left * random.randint(18, 22) / 20), offset_y,
                         duration = random.randint(19, 31) / 100)
        offset_y += random.randint(0, 8)
        pyautogui.moveTo(offset_x + int(left * random.randint(19, 21) / 20), offset_y,
                         duration = random.randint(20, 40) / 100)
        offset_y += random.randint(-3, 3)
        pyautogui.moveTo(left + offset_x + random.randint(-3, 3), offset_y,
                         duration = 0.5 +random.randint(-10, 10) / 100)
        offset_y += random.randint(-2, 2)
        pyautogui.moveTo(left + offset_x + random.randint(-2, 2), offset_y,
                         duration = 0.5 +random.randint(-3, 3) / 100)
        pyautogui.mouseUp()
        time.sleep(3)







    def close_browser(self):
        self.driver.quit()


    def main(self):
        self.get_to_website()
        self.switch_to_main_window()
        self.get_captcha()
        self.gap_pic_ele_change()
        self.screen_shot('gap.png')
        self.intact_pic_ele_change()
        self.screen_shot('intact.png')
        # left = self.get_gap('gap.png', 'intact.png') * 2 - 14 # 此项目的开发环境缩放为200%，再手动减去偏差
        # 没卵用
        # track = self.get_track(left)
        # slide_tag = self.driver.find_element(By.CLASS_NAME, 'geetest_slider_button')
        # ActionChains(self.driver).click_and_hold(slide_tag).perform()
        # for x in track:
        #     ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        # time.sleep(0.5)
        # ActionChains(self.driver).release().perform()
        left = self.get_gap('gap.png', 'intact.png') * 2 - 14
        self.restore_style()
        self.move_slide(1043, 895, left) # 坐标需要自行调整
        self.close_browser()
        self.driver.quit()


if __name__ == '__main__':
    slide = Slide()
    slide.main()
