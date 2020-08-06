# -*- coding:utf-8 -*-
"""
@Author:    beiyue
@Contact:   beiyue_z@foxmail.com
@File:  01第一步爬取租房信息.py
@Time:  2020/7/29 19:02
@Tools: PyCharm
@Desc:  
"""

import pandas as pd
import requests
import re
import time

data_zf_list = pd.DataFrame(columns=['area','shi','wei','ting','price_per_month'])
count = 0
url = 'https://gy.lianjia.com/zufang/huaxiqu/pg'
page = 1

# 1.选择一个网站，从这个网站爬去相关数据（数据有一定的线性关系）
def getHtmlText(link):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
    response = requests.get(link,headers=headers)
    response.raise_for_status()  # 如果状态码不是200，会引发HTTPerror异常
    response.encoding = response.apparent_encoding
    return response.text

def parserHtmlText(html):
    global data_zf_list,count,page
    # selector = etree.HTML(html)
    # selector.xpath("//div[@class='content__list--item']/div[@class='content__list--item--main']")
    all_div = re.findall('<p class="content__list--item--des">(.*?)</div>',html,re.S)
    for each in all_div:
        area = re.search('\s(\d+)㎡',each).group(1)
        info = re.search('\s(\d)室(\d)厅(\d)卫',html)
        shi = info[1]
        wei = info[2]
        ting = info[3]
        price = re.search('<em>(\d+)</em>',each).group(1)
        data_zf_list.loc[len(data_zf_list)] = [area,shi,wei,ting,price]
    count += len(all_div)
    print('已经爬取第'+str(page)+'页'+' 共'+str(count)+'条数据')

def startCrawl():
    global page
    start = time.time()
    while True:
        # 读取网页，返回回来html
        html = getHtmlText(url+str(page))
        if html.find('没有找到相关房源，可以尝试调整搜索条件') != -1:
            print("搜索结束，欢迎使用！")
            break
        # 解析网页，把抓取到的数据存储下来
        parserHtmlText(html)
        page += 1
    print('恭喜爬取数据成功')
    end = time.time()
    print("共耗时"+str(end-start)+'秒')
    writeZFCsv()

def writeZFCsv():
    global data_zf_list
    data_zf_list.to_csv('huaxi_zf.csv',encoding='utf-8_sig',index=False)
    print('数据写入成功！')

if __name__ == '__main__':
    startCrawl()