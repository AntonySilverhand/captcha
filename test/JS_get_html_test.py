from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options


# Set up the driver
driver = webdriver.Edge()  # or webdriver.Chrome(), depending on your browser
chrome_options = Options()

# 创建Edge WebDriver 选项
options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument('--headless--')
options.add_argument('--disable-gpu')
options.add_argument(
    "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'")        # 去掉识别
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('detach', True)
# 去掉window.navigator.webdriver的特性
options.add_argument('disable-blink-feature = AutomationControlled')
# 添加referer
options.add_argument("Referer='https://www.bing.com/'")

# Open the page
driver.get('https://www.douban.com/')

# Wait for the page to load by checking for the visibility of the text added by ::after
wait_time = 10  # seconds
end_time = time.time() + wait_time
while time.time() < end_time:
    try:
        # Execute JavaScript to check if the text is visible
        result = driver.execute_script("""
            var parentEl = document.querySelector('.parent-selector'); // replace with the correct selector
            var text = window.getComputedStyle(parentEl).getPropertyValue('content');
            return text.trim().length > 0;
        """)
        if result:
            break
    except Exception as e:
        pass
    time.sleep(0.5)  # wait half a second before trying again

print(driver.page_source)

# Now you can proceed with the rest of your script knowing that the ::after content is visible
# ...

# Don't forget to close the driver when you're done
driver.quit()
