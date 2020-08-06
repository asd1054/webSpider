# -*- coding: utf-8 -*-
"""
@Author       : wukong
@Date         : 2020-03-07 18:41:40
@Description  : 多任务批量下载视频
@blog         : https://asd1054.github.io/
@Github       : https://github.com/asd1054
@version      : 1.0
"""
from multiprocessing import Pool
import os
import subprocess


def splitNum(start, end, step=0):
    """
    @description: 
        用来切断范围，好返回一个列表用来 分批下载

    @params: 
        开始和结束的番数
        step 起始为0，则至少每个进程1个以上
    """
    split_tuple = []
    tmp = start
    for i in range(9):
        split_tuple.append((tmp, tmp + step))
        tmp = tmp + step + 1
        if tmp >= end:
            break
    if tmp <= end:
        split_tuple.append((tmp, end))
    return split_tuple


def worker(start, end):
    url = "https://www.bilibili.com/video/BV1Pp411d7Vy?p="  # 程序的设置点2   设置网址
    pathname = '文件夹名字'  # 程序设置点3 下载路径
    for i in range(start, end + 1):
        subprocess.Popen(
            "activate p37 & you-get -o {pathname} --no-caption {url}{p}".format(
                url=url, p=i, pathname=pathname
            ),
            shell=True,
        )
    print(os.getpid(), "正在进行任务", start, end)


def main():
    p = Pool(10)
    step = splitNum(1, 214, step=20)  # 程序的设置点1 设置下载的番数,step每个进程需要负责的几个
    try:
        for i in range(10):
            p.apply_async(worker, (step[i][0], step[i][1],))
    except Exception as e:
        print(e)  # 防止下载的视频数少于20个
    print("***********任务开始***********")
    p.close()  # 关闭进程池
    p.join()
    print("*********所有任务结束*********")


if __name__ == "__main__":
    main()
