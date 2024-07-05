"""
目标网站：http://www.51job.com

需求：
1.点击 职位搜索
2.输入关键字 python
3.地区选择 广州
4.职能类别选择 计算机 --> 后端开发 ---> python开发工程师
5.工作年限选择 1-3年
6.抓取到所有的岗位标题和里面的职位信息
7.保存到csv
"""



from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# 创建Edge WebDriver 选项
options = webdriver.EdgeOptions()
options.use_chromium = True
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0")
# 去掉识别
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('detach',True)
# 去掉window.navigator.webdriver的特性
options.add_argument('disable-blink-feature = AutomationControlled')

# 创建 Edge 浏览器对象
driver = webdriver.Edge(options = options)
time.sleep(random.random()*2)

# 到达目标网站
driver.get('http://www.51job.com')
time.sleep(random.random()*2)

# 获取当前窗口句柄
main_window = driver.current_window_handle

# 获取当前所有窗口的句柄
all_windows = driver.window_handles

# 条件判断
for handles in all_windows:
    if handles == main_window:
        continue
    else:
        driver.switch_to.window(handles)
        driver.close()

driver.switch_to.window(main_window)

#0. 设置等待以及等待页面加载完毕
driver.implicitly_wait(10)

# 1.点击 职位搜索
driver.find_element(By.XPATH, "//p[@class = 'nlink']/a[2]").click()
time.sleep(random.random()*2)

# 2.输入关键字 python
driver.find_element(By.XPATH, "//p[@class = 'nlink']/a[2]").send_keys("python")
time.sleep(random.random()*2)

# 2.5 去掉窗口
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.RETURN)

# 3.地区选择 广州
driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]').click()
time.sleep(random.random()*2)
driver.find_element(By.XPATH, '//*[@id="pane-0"]/div/div/div[3]/span').click()
time.sleep(random.random()*2)
driver.find_element(By.XPATH, '//*[@id="dilog"]/div/div[3]/span/button/span').click()
time.sleep(random.random()*2)







# 错误测试












try:
    # 4.职能类别选择 计算机 --> 后端开发 ---> python开发工程师
    driver.find_element(By.LINK_TEXT, "工作职能").click()
    time.sleep(random.random()*2)
    driver.find_element(By.XPATH, '//*[@id="dialog_1702032866404"]/div/div[2]/div[2]/ul[1]/li[2]/div/span').click()
    time.sleep(random.random()*2)
    driver.find_element(By.XPATH, '//*[@id="dialog_1702032866404"]/div/div[2]/div[2]/ul[2]/li[1]/div/span').click()
    time.sleep(random.random()*2)
    driver.find_element(By.XPATH, '//*[@id="dialog_1702032866404"]/div/div[2]/div[2]/ul[3]/li[11]/div/span').click()
    time.sleep(random.random()*2)
    driver.find_element(By.XPATH, '//*[@id="dialog_1702032866404"]/div/div[3]/div/button[2]/span').click()
    time.sleep(random.random()*2)

except NoSuchElementException:
    print("元素未找到，可能网页结构已经改变或者元素尚未加载")
finally:
    # 5.工作年限选择 1-3年
    driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[1]/div[2]/div[4]/span').click()
    time.sleep(random.random()*2)
    driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[1]/div[2]/div[3]/div[1]/div/div[2]/a[3]/span').click()
    time.sleep(random.random()*2)

    # 6.抓取到所有的岗位标题和里面的职位信息


    driver.close()
    driver.quit()
