# coding:utf-8
'''
@Author:    beiyue
@Contact:   beiyue_z@foxmail.com
@File:  001教务系统登录(有隐私信息）.py
@Time:  2020/7/25 16:28
@Desc:  模拟登录教务系统，进行信息查询等操作
'''

from bs4 import BeautifulSoup
import requests
# from pytesseract import *
# from PIL import Image
import time


class Spider:
    """写 一个爬虫的模板
    具有读取网页，解析网页，下载网页等基本功能
    """

    def __init__(self, url='http://210.40.2.253:8888', xh='学生学号', pwd='学生密码'):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'})
        self.html = self.getHtmlText(self.url)
        self.xh = xh
        self.pwd = pwd

    def getLogin(self):
        __VIEWSTATE = self.getHinddenValue()
        self.getTxtSecretCode()
        # 无法为透明度分配调色板条目
        # image = Image.open('code.png')
        # txtSecretCode = image_to_string(image)
        # print(txtSecretCode)
        txtSecretCode = input('请输入图片验证码：')
        data = {
            '__VIEWSTATE': __VIEWSTATE,
            'txtUserName': self.xh,
            "Textbox1": '',
            'TextBox2': self.pwd,
            'txtSecretCode': txtSecretCode,
            'RadioButtonList1': '%D1%A7%C9%FA',
            'Button1': '',
            'lbLanguage': '',
            'hidPdrs': '',
            'hidsc': ''
        }
        self.base_html = self.postHtmlText(self.url, data)
        return self.base_html

    def getPerson(self):
        # TODO 抓取个人基本信息
        soup = BeautifulSoup(self.base_html, 'html.parser')
        tmp = soup.find('span', 'xhnm')
        print(tmp)

    def getTxtSecretCode(self):
        with open('code.png', 'wb') as fw:
            response = self.session.get(self.url+'/CheckCode.aspx')
            fw.write(response.content)

    def getHinddenValue(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        __VIEWSTATE = soup.find(
            'input', attrs={'type': "hidden", 'name': '__VIEWSTATE'}).get('value')
        # print(__VIEWSTATE)
        return __VIEWSTATE

    def getHtmlText(self, url):
        response = self.session.get(url)
        response.raise_for_status()  # 如果状态码不是200，会引发HTTPerror异常
        response.encoding = response.apparent_encoding
        self.html = response.text
        return self.html

    def postHtmlText(self, url, data=None):
        response = self.session.post(url, data=data)
        response.raise_for_status()  # 如果状态码不是200，会引发HTTPerror异常
        response.encoding = response.apparent_encoding
        self.html = response.text
        return self.html

    def start(self):
        success = False
        while not success:
            print('正在登录系统中')
            html = self.getLogin()
            pd = html.find('退出')
            if pd != -1:
                success = True
                print('恭喜登录成功！')
            else:
                print('请重新检查验证码，或者用户名，或者密码')
                time.sleep(2)

    def test(self):
        url = self.url+'/xs_main.aspx?xh=%s' % self.xh
        html = self.getHtmlText(url)
        print(html)


if __name__ == '__main__':
    education_system = Spider('http://210.40.2.253:8888')
    education_system.start()
    # print(education_system.html)
    # education_system.test()
    education_system.getPerson()
