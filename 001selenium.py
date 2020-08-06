# -*- coding:utf-8 -*-
"""
@Author:    beiyue
@Contact:   beiyue_z@foxmail.com
@File:  001selenium.py
@Time:  2020/7/27 14:15
@Envir: PyCharm
@Desc:  
"""

from selenium import webdriver

driver = webdriver.PhantomJS()

driver.get('http://wwww.baidu.com/')
# driver.save_screenshot('baidu.png')

# 搜索框搜索“美女”
driver.find_element_by_id('kw').send_keys('美女')
# driver.save_screenshot('baidu.png')

# 点击搜索按钮
driver.find_element_by_id('su').click()
driver.save_screenshot('baidu.png')
