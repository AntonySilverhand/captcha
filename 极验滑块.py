from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service


class Slide():
    def __init__(self):
        # 实操中需要传入用户名和密码
        self.options = webdriver.EdgeOptions()
        self.options.use_chromium = True
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        # 去掉识别
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('detach', True)
        # 去掉window.navigator.webdriver的特性
        self.options.add_argument('disable-blink-feature = AutomationControlled')

        self.options.add_argument("user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0")
        # self.edge_driver_path = r'E:\edge_driver'
        self.driver = webdriver.Edge(options = self.options)

        self.url = 'https://www.geetest.com/demo/slide-float.html'

        # 窗口最大化
        try:
            self.driver.maximize_window()
        except:
            pass

        # 显式等待
        self.wait = WebDriverWait(self.driver, 100)


    # 获取验证码
    def get_captcha(self):
        self.driver.get(self.url)

        btn_tag = self.wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_radar_tip_content'), '点击按钮进行验证')
        )
        self.driver.find_element(By.CLASS_NAME, 'geetest_radar_tip_content').click()

    def get_gap(self):
        pass

    def move_slide(self):
        pass

    def main(self):
        self.get_captcha()


if __name__ == '__main__':
    slide = Slide()
    slide.main()