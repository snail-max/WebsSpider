# -*-coding:utf-8-*-

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# 规避检测风险
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions



# 创建一个浏览器对象，控制chrome以无界面的方式打开
chrome_options = Options()
chrome_options.add_argument('----headless')
chrome_options.add_argument('--disable-gpu')


# 规避检测风险
option = ChromeOptions()
# 'excludeSwitches', ['enable-automation']
option.add_experimental_option('excludeSwitches', ['enable-automation'])
# driver = Chrome(options=options)

# 驱动路径
chrome_path = '../chromedriver.exe'
# 如何实现selenium避免被检测到的风险
bro = webdriver.Chrome(executable_path=chrome_path,options=option,chrome_options=chrome_options)

# 无可视化界面
bro.get('https://www.baidu.com')
time.sleep(3)
bro.save_screenshot('baidu.png')
bro.quit()

