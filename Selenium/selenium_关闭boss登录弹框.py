# -*-coding:utf-8-*-
from selenium import webdriver
import time




driver = webdriver.Chrome(executable_path='../chromedriver.exe')


driver.get("https://www.zhipin.com/job_detail/?query=Python&city=101020100&industry=&position=")
time.sleep(1)
js = 'document.getElementsByTagName("script")[0].style.display="none"'
driver.execute_script(js)
print(driver.save_screenshot('./aa.jpg'))