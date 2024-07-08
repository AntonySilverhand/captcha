from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 实操中需要传入用户名和密码
options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument('--headless')
options.add_argument('--disable-gpu')
# 去掉识别
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('detach', True)
# 去掉window.navigator.webdriver的特性
options.add_argument('disable-blink-feature = AutomationControlled')

options.add_argument("user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0")

driver = webdriver.Edge(options = options)

url = 'https://www.geetest.com/demo/slide-float.html'


driver.get(url)

# 显式等待
wait = WebDriverWait(driver, 100)
# 窗口最大化
try:
    driver.maximize_window()
except:
    pass

btn_tag = wait.until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip_content'))
)
btn_tag.click()