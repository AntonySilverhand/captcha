"""
可以得到原图，缺口，滑块
"""


import time
import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from 缺口偏移量计算 import get_gap
from 人性化滑动 import move_slide
from opencv缺口识别 import indentify_gap

import sys




class Slide:
    def __init__(self, username, password):


        self.username = username
        self.password = password


        # 创建Edge WebDriver 选项
        self.options = webdriver.EdgeOptions()
        self.options.use_chromium = True
        # self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'")        # 去掉识别
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('detach', True)
        # 去掉window.navigator.webdriver的特性
        self.options.add_argument('disable-blink-feature = AutomationControlled')
        # 添加referer
        self.options.add_argument("Referer='https://www.bing.com/'")

        # 创建 Edge 浏览器对象
        self.driver = webdriver.Edge(options=self.options)
        self.url = 'https://www.douban.com/'

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
        self.driver.maximize_window()


    def login(self):
        time.sleep(1.1)

        actions = ActionChains(self.driver)
        actions.move_by_offset(930, 164).click().perform()
        time.sleep(random.uniform(0.1, 1.8))

        actions.move_by_offset(3, 72).click().perform()
        time.sleep(random.uniform(0.1, 1.8))
        actions.send_keys(self.username).perform()
        time.sleep(random.uniform(0.1, 1.0))

        actions.move_by_offset(-5, 56).click().perform()
        time.sleep(random.uniform(0.1, 1.8))
        actions.send_keys(self.password).perform()
        time.sleep(random.uniform(0.1, 1.8))


        actions.move_by_offset(2, 48).click().perform()


    def ele_load(self):

        js_code = """
        var element = document.querySelector('.account-tab-account');
        element.click();
        """
        content = self.driver.execute_script(js_code)




    def screen_shot(self, name):
        # 截图
        """
        使用CSS时不要预先定义再传入，会报string错误，直接在参数里写定位器
        """
        # 等待图片加载完成后截图
        time.sleep(1)
        self.captcha_tag = self.driver.find_element(By.CLASS_NAME, 'tc-opera')
        self.captcha_tag.screenshot(name)
        print(name, "截图成功")


    def get_captcha(self):


        self.locator_click = (By.CSS_SELECTOR, '.btn btn-account.btn-active"')
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
        self.locator_slider_tip = (By.CSS_SELECTOR, '.tc-fg-item.tc-slider-normal') # 定位目标含有空格时使用class会报错，有两种解决方法，其一是以空格为分割，选择最长的那串，其二是使用css并且将空格改为点.此外开头也需要加.
        self.slide_tag = self.wait.until(
            EC.element_to_be_clickable(self.locator_slider_tip)
        )


        # 检查滑块是否可见和可点击
        if self.slide_tag.is_displayed() and self.slide_tag.is_enabled():
            print("Slider is displayed and enabled.")

        else:
            print("Slider is not displayed or not enabled. Process killed.")
            # 终止代码
            self.driver.quit()


    def get_intact_pic(self):
        self.intact_pic = self.screen_shot('intact_pic.png')

    def get_gap_pic(self):
        # 将滑块不透明度改为0，得到缺口
        self.driver.execute_script('document.querySelectorAll("div.tc-fg-item")[2].style="position: absolute; background-image: url(&quot;https://turing.captcha.qcloud.com/cap_union_new_getcapbysig?img_index=0&image=0279050000696e120000000bb95916f52f4c&sess=s0fJw9DDTXzlIrngKiB3sqv2hc93CSEuA397_EtlwHQgLZwLHAD9AXBOm8XOFXp-uUj04GW8nOhGtiH1053LibSyrEJUlvEo9Q0rcmE4IfFmBBL3sKX8Dy115w7EOZnuxdmPbm6QxvA_7Txju9ThrL9ePn02n2Cg2xnnjTrrjYwRJB8oV13qGJSiaufwsMhlRM_mT79BLIv6jMPKZgsfGYjRfBEyAFZfL1SJ43YHbNpaYLBpmhmO9Lrw8HY8GmFjeyGheAn6HUIRywId5c9xescRVAgMHFkzxrN17H3_4cID7wuXtGprfqymO_JE5t4hacS9uPVVc9vrWRSJkcW3_6cqoqQ3-is2FrY15gQX0Kd5d6fwf23iBj2JzjyH58I8IHXMcpZielqMX04v1A8kIBMm7IG-nwHp9om7_S6xdNYp1snzNx44_tqw**&quot;); background-position: -57.9167px -202.708px; background-size: 282.137px 256.488px; width: 49.6429px; height: 49.6429px; left: 20.6845px; top: 42.6101px; z-index: 1; cursor: pointer; opacity: 0;"')
        self.gap_pic = self.screen_shot('gap_pic.png')


    def get_slider_pic(self):
        # 将背景图片（缺口）不透明度改为0，得到滑块
        self.driver.execute_script('document.querySelectorAll("div.tc-bg-img.unselectable").style="position: absolute; background-image: url(&quot;https://turing.captcha.qcloud.com/cap_union_new_getcapbysig?img_index=1&image=02790500005c33620000000bb95916f52f54&sess=s0jQuxTx5jhb_Uvu_VhJN_qSP7X_alGjK4RU4syam_XDoJl3LGY6lcqCN14JEbHYbC_4leBEjdKt1Nd7waoM-Rkbd29QL-_j02SvIzINmZgw9iOVhiL5y6Me6LvShoy-KYgRUb3BDaVYeORRSKePxA7JP3an_Xs2gjcE7tvFYoF32GSKn9vffIC_XyaHSw-95KtaRyIly1ApzXW87DbW58lzOXaOC28td-4YU-YRFPx70SWWHuaVVsO3WIzHuQSzGDn1L3aDFoj8nM9o-uasqaSRWoqCDJ66habHiofQw80C9qEVRw51OyGEn_9DXEixmc6hd3YQPt7ULcUnVV6MORQnZvQWK3UtlCf71FWGXMnIss8-w8OSFBWdaX8uSeerZ_WzvjJVR9NvJuZkBKlycHzYsl9zBPBEmmltkUwwk22odOwVIeMJizoA**&quot;); background-position: 0px 0px; background-size: 100%; width: 278px; height: 198.571px; left: 0px; top: 0px; background-repeat: no-repeat; overflow: hidden; z-index: 1; opacity: 0;"')
        self.slider_pic = self.screen_shot('slider_pic.png')

    def restore_style(self):
        # 恢复样式
        self.driver.execute_script('document.querySelectorAll("div.tc-fg-item")[2].style="position: absolute; background-image: url(&quot;https://turing.captcha.qcloud.com/cap_union_new_getcapbysig?img_index=0&image=0279050000696e120000000bb95916f52f4c&sess=s0fJw9DDTXzlIrngKiB3sqv2hc93CSEuA397_EtlwHQgLZwLHAD9AXBOm8XOFXp-uUj04GW8nOhGtiH1053LibSyrEJUlvEo9Q0rcmE4IfFmBBL3sKX8Dy115w7EOZnuxdmPbm6QxvA_7Txju9ThrL9ePn02n2Cg2xnnjTrrjYwRJB8oV13qGJSiaufwsMhlRM_mT79BLIv6jMPKZgsfGYjRfBEyAFZfL1SJ43YHbNpaYLBpmhmO9Lrw8HY8GmFjeyGheAn6HUIRywId5c9xescRVAgMHFkzxrN17H3_4cID7wuXtGprfqymO_JE5t4hacS9uPVVc9vrWRSJkcW3_6cqoqQ3-is2FrY15gQX0Kd5d6fwf23iBj2JzjyH58I8IHXMcpZielqMX04v1A8kIBMm7IG-nwHp9om7_S6xdNYp1snzNx44_tqw**&quot;); background-position: -57.9167px -202.708px; background-size: 282.137px 256.488px; width: 49.6429px; height: 49.6429px; left: 20.6845px; top: 42.6101px; z-index: 1; cursor: pointer; opacity: 1;"')
        self.driver.execute_script('document.querySelectorAll("div.tc-bg-img.unselectable").style="position: absolute; background-image: url(&quot;https://turing.captcha.qcloud.com/cap_union_new_getcapbysig?img_index=1&image=02790500005c33620000000bb95916f52f54&sess=s0jQuxTx5jhb_Uvu_VhJN_qSP7X_alGjK4RU4syam_XDoJl3LGY6lcqCN14JEbHYbC_4leBEjdKt1Nd7waoM-Rkbd29QL-_j02SvIzINmZgw9iOVhiL5y6Me6LvShoy-KYgRUb3BDaVYeORRSKePxA7JP3an_Xs2gjcE7tvFYoF32GSKn9vffIC_XyaHSw-95KtaRyIly1ApzXW87DbW58lzOXaOC28td-4YU-YRFPx70SWWHuaVVsO3WIzHuQSzGDn1L3aDFoj8nM9o-uasqaSRWoqCDJ66habHiofQw80C9qEVRw51OyGEn_9DXEixmc6hd3YQPt7ULcUnVV6MORQnZvQWK3UtlCf71FWGXMnIss8-w8OSFBWdaX8uSeerZ_WzvjJVR9NvJuZkBKlycHzYsl9zBPBEmmltkUwwk22odOwVIeMJizoA**&quot;); background-position: 0px 0px; background-size: 100%; width: 278px; height: 198.571px; left: 0px; top: 0px; background-repeat: no-repeat; overflow: hidden; z-index: 1; opacity: 1;"')



    def way_1(self): # 原图+缺口
        self.get_intact_pic()
        self.get_gap_pic()
        self.restore_style()
        left = get_gap(self.intact_pic, self.gap_pic)
        move_slide(left = left)  # 需要填写坐标


    def way_2(self): # 原图+滑块
        self.get_intact_pic()
        self.get_slider_pic()
        self.restore_style()
        left = indentify_gap(self.intact_pic, self.slider_pic)
        move_slide(left = left)  # 需要填写坐标


    def quit(self):
        self.driver.quit()





    def run(self):
        self.get_to_website()
        self.switch_to_main_window()
        time.sleep(5)
        self.ele_load()
        #self.login()
        # self.get_captcha()
        time.sleep(5)
        self.quit()





if __name__ == '__main__':
    slide = Slide('16327754698', '789465132')
    slide.run()

    