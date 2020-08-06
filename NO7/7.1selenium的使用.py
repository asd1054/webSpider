from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.wait import WebDriverWait

brower = webdriver.Chrome()
try:
    url = 'http://baidu.com'
    brower.get(url)
    input = brower.find_element_by_id('mq')
except Exception:
    print("errors")