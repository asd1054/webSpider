# -*- coding:utf-8 -*-
"""
@Author:    beiyue
@Contact:   beiyue_z@foxmail.com
@File:  start.py
@Time:  2020/7/27 23:19
@Tools: PyCharm
@Desc:  
"""

from scrapy import cmdline

# cmdline.execute('scrapy crawl itcast_teachers -o tearchers_new.csv'.split())
cmdline.execute('scrapy crawl itcast_teachers'.split())