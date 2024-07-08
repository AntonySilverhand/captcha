# test_slide.py
import unittest
from unittest.mock import patch, MagicMock
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 导入待测试对象
from test_rewrite_from_selenium必做题 import Slide

class TestSlide(unittest.TestCase):
    @patch('selenium_captcha.Slide.wait')
    def test_get_captcha(self, mock_wait):
        # 创建一个mock对象来模拟元素
        mock_element = MagicMock()
        # 当等待条件满足时，返回mock元素
        mock_wait.until.return_value = mock_element

        # 创建driver mock
        mock_driver = MagicMock(spec=webdriver.Chrome)
        # 模拟maximize_window方法
        mock_driver.maximize_window.return_value = None

        # 初始化Slide对象，并注入mock的driver
        slide = Slide()
        slide.driver = mock_driver

        # 运行get_captcha方法
        slide.get_captcha()

        # 测试是否调用了maximize_window
        mock_driver.maximize_window.assert_called_once()

        # 测试是否正确构造了等待的条件
        mock_wait.until.assert_called_once_with(
            EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip_content'))
        )

        # 测试是否点击了按钮
        mock_element.click.assert_called_once()

if __name__ == '__main__':
    unittest.main()
