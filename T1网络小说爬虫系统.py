# coding:utf-8
'''
@Author:    beiyue
@Contact:   beiyue_z@foxmail.com
@File:  T1网络小说爬虫系统.py
@Time:  2020/7/24 13:59
@Desc:  
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import sys
import pickle
import os
from tqdm import tqdm

class Spider:
    """写 一个爬虫的模板
    具有读取网页，解析网页，下载网页等基本功能
    """
    def __init__(self, url='http://baidu.com',search='http://baidu.com'):
        self.url = url
        self.search = search
        self.getHtmlText()

    def getHtmlText(self):
        try:
            ua_list = [
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
                'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
                'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
            ]
            user_agent = random.choice(ua_list)
            headers = {'User-Agent': user_agent}
            r = requests.get(self.url, timeout=30, headers=headers)
            r.raise_for_status()  # 如果状态码不是200，会引发HTTPerror异常
            r.encoding = r.apparent_encoding
            self.html = r.text
            return self.html
        except:
            return "产生异常"

    def getSearchHtmlText(self):
        keyword = input('请输入要搜索的关键词：')
        keywords ='keyword='+keyword
        tmp = self.url
        self.url = self.search+keywords
        self.getHtmlText()
        self.url = tmp
        return self.html

    def downloadHtmlText(self):
        with open('data.txt', 'w', encoding='utf-8') as f:
            f.write(self.html)
        print('下载信息成功')


class WebNovel(Spider):
    '''用来爬取《米趣小说》网的小说'''

    def __init__(self, url='https://www.meegoq.com/',search = 'https://www.meegoq.com/search.htm?'):
        super().__init__(url,search)
        self.catalog = pd.DataFrame(columns=['标题', '网址'])

    def getCatalogList(self):
        print('{:*^35}'.format('爬取目录中'))
        self.getHtmlText()
        soup = BeautifulSoup(self.html, 'html.parser')
        mu_list = soup.find('ul', 'mulu')
        mu_list = mu_list.find_all('a')
        print('共发布了'+str(len(mu_list)-9)+'个章节')
        for i in range(10, len(mu_list)):
            chapter = mu_list[i]
            url = 'https://'+chapter['href'][2:]
            title = chapter.text
            self.catalog.loc[len(self.catalog)] = [title, url]
        print('目录爬取成功')

    def getSearchHtmlText(self):
        keyword = input('请输入书名或者作者：')
        keywords ='keyword='+keyword
        tmp = self.url
        self.url = self.search+keywords
        self.getHtmlText()
        self.url = tmp
        return self.html

    def getSearchList(self):
        print('{:*^35}'.format('返回搜索结果：'))
        soup = BeautifulSoup(self.html, 'html.parser')
        result = soup.find(name='section',attrs={'class':'lastest'})
        result = result.find_all('li')
        self.results = pd.DataFrame(columns = ["分类", "名称", "最新章节", "作者",'url'])
        for i in range(1,len(result)):
            line = result[i]
            try:
                span = line.span.fetchNextSiblings()
            except Exception as e:
                break
            classify = line.span.string
            name =span[0].string
            url = 'https://'+span[0].a.get('href')[2:]
            url = url.replace('info','book')
            lastest = span[1].string
            author = span[2].string
            self.results.loc[len(self.results)] = [classify,name,lastest,author,url]
        return self.results

    def getMainBody(self):
        self.getHtmlText()
        soup = BeautifulSoup(self.html, 'html.parser')
        result = soup.find(name='div',attrs={'class':'content'})
        content = result.text
        content.replace('　　','\n')
        return content

    def catalogToCsv(self,name):
        '''保存小说的章节目录以及url地址'''
        print('{:*^35}'.format('保存数据中'))
        self.getCatalogList()
        self.catalog.to_csv('./novel/'+name+'.csv', index=False)
        print('小说目录保存成功，请到本地文件夹中进行查看！')

class NovelMenu:
    def __init__(self):
        self.cord = pd.DataFrame(columns=['小说名字','作者','小说地址'])
        self.novel = WebNovel()

    def welcome(self):
        print('{:*^35}'.format('【免费小说阅读系统】'))
        print('*' * 40)
        print('1.搜索小说')
        print('2.关于作者')
        print('3.搜索记录')
        print('0.退出系统')
        print('PS：本系统均是在https://www.meegoq.com进行阅读')
        print('*' * 40)
        self.ch = int(input('请选择你的操作：'))


    def subQuery(self):
        print('{:*^35}'.format('正在搜索小说信息'))
        self.novel.getSearchHtmlText()
        results = self.novel.getSearchList()
        print(results)
        print("当输入99的时候，返回主菜单")
        ch = int(input('请选择你的操作(输入行号)：'))
        url = results.loc[ch].url
        self.novel.url = url
        self.now = [results.loc[ch]['名称'],results.loc[ch]['作者'],results.loc[ch].url]
        self.novel_name = self.now[0]
        self.cord.loc[len(self.cord)] = self.now
        if ch == 99:
            return
        else:
            self.thirdLevel()

    def thirdLevel(self):
        print('{:*^35}'.format('正在进行小说操作'))
        print('1.下载小说章节目录')
        print('2.下载小说详细内容')
        print('0.返回主菜单')
        ch = int(input('请选择你的操作(输入行号)：'))
        if ch == 1:
            self.novel.catalogToCsv(self.novel_name)
        elif ch == 2:
            self.downloadMainBody()
        elif ch ==0:
            return



    def downloadMainBody(self):
        print('{:*^35}'.format('正在下载小说'))
        self.novel.getCatalogList()
        fw = open('./novel/'+self.now[0]+'.txt','w',encoding='utf-8')
        fw.write(self.now[0]+'\n')  # 小说名字
        fw.write(self.now[1]+'\n')  # 小说作者
        fw.write(self.now[2]+'\n')  # 小说地址

        for i in tqdm(range((self.novel.catalog.shape[0]))):
            url = self.novel.catalog['网址'][i]
            chapter = self.novel.catalog['标题'][i]
            self.novel.url = url
            content = self.novel.getMainBody()
            fw.write(chapter+'\n')
            fw.write(content+'\n')
            fw.write('\n')
        fw.close()
        print('下载《'+self.now[0]+'》小说成功')


    def getCh(self):
        return self.ch

    def aboutMe(self):
        print('system created by beiyue')
        print('contacted by beiyue_z@foxmail.com')

    def viewCord(self):
        print(self.cord)
        # print(self.cord.keys().values)
        # print(self.cord.values().values)
    def subViewCord(self):
        self.viewCord()
        print("当输入99的时候，返回主菜单")
        ch = int(input('请选择你的操作(输入行号)：'))
        if ch == 99:
            return
        url = self.cord.loc[ch]['小说地址']
        self.novel_name = self.cord.loc[ch]['小说名字']
        self.now = self.cord.loc[ch].values
        self.novel.url = url
        self.thirdLevel()


    def getState(self):
        state = {1: self.subQuery, 2: self.aboutMe, 3: self.subViewCord, 0: self.exit}
        return state[self.ch]()


    def saveData(self):
        self.cord.to_csv('cord.profile',index=False)
        print('保存cord数据成功!')

    def loadData(self):
        if os.path.exists("cord.profile"):
            self.cord = pd.read_csv('cord.profile')
            print("加载cord数据成功!")


    def exit(self):
        self.saveData()
        sys.exit('谢谢使用，再见！')

    def main(self):
        if os.path.exists("cord.profile"):
            self.loadData()
        if not os.path.exists("novel"):
            os.mkdir('novel')
        while True:
            try:
                self.welcome()
                self.getState()
                input('请输入回车键继续。。。')
            except Exception as e:
                print(e)
                print('发现一个异常错误')

if __name__ == '__main__':
    menu = NovelMenu()
    menu.main()