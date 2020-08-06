# -*- coding:utf-8 -*-
"""
@Author:    beiyue
@Contact:   beiyue_z@foxmail.com
@File:  02第二步线性回归.py
@Time:  2020/7/29 19:49
@Tools: PyCharm
@Desc:  
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def main():

    # 读取数据
    data = pd.read_csv('huaxi_zf.csv')

    # 2.组织样本数据（X）和标签数据（y）
    X = data[['area','shi','wei','ting']] # 4.至少选择2个维度以上
    Y = data['price_per_month']

    # 3.对样本数据进行测试集和训练集的划分
    x_train, x_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.3, random_state=4420) # 4420

    # 5.使用训练集训练出模型
    linear_model = LinearRegression()
    linear_model.fit(x_train,y_train)

    # 6.对训练的模型进行评估（r2 = lin_reg.score(X_test,y_test)），越大越好
    score = linear_model.score(x_test, y_test)
    print("模型测试集分数:" + str(score))


    # 系数
    print(linear_model.coef_)
    # 截距
    print(linear_model.intercept_)


if __name__ == '__main__':
    main()