# coding:utf-8
'''
@Author:    beiyue
@Contact:   beiyue_z@foxmail.com
@File:  002学生信息管理系统2.0.py
@Time:  2020/7/22 16:32
@Desc:  
'''

import sys
import pickle
from prettytable import PrettyTable
import pandas as pd


class Student:
    def __init__(self, sid=1, sname=None, sex=None, score=None):
        self.__sid = sid
        self.__sname = sname
        self.__sex = sex
        self.__score = score

    @property
    def Sid(self):
        return self.__sid

    @Sid.setter
    def Sid(self, sid):
        self.__sid = sid

    @property
    def Sname(self):
        return self.__sname

    @Sname.setter
    def Sname(self, sname):
        self.__sname = sname

    @property
    def Sex(self):
        return self.__sex

    @Sex.setter
    def Sex(self, sex):
        self.__sex = sex

    @property
    def Score(self):
        return self.__score

    @Score.setter
    def Score(self, score):
        self.__score = score

    def showStudent(self):
        table = PrettyTable(["学号", "姓名", "性别", "分数"])
        table.add_row([self.Sid, self.Sname, self.Sex, self.Score])
        print(table)

class DataBase:
    """实现增删改查功能"""
    def insertStudent(self):
        print('{:*^35}'.format('正在添加学生信息'))
        print('{:*^35}'.format('学号自动添加'))
        name = input('请输入学生姓名：')
        sex = input('请输入学生性别：')
        score = input('请输入学生分数：')
        print('操作成功！')
        student = Student()
        student.Sid = self.sid
        student.Sname = name
        student.Sex = sex
        student.Score = score
        self.lst.append(student)
        self.sid += 1

    def deleteStudent(self):
        print('{:*^35}'.format('正在删除学生信息'))
        sid = int(input('请输入要删除的学生学号：'))
        i = 0
        for student in self.lst:
            if student.Sid == sid:
                self.lst.pop(i)
                print('操作成功！')
                return
            i += 1
        print('该学号尚未注册,删除失败')


    def showAllStudent(self,tmp_lst=None):
        print('{:*^35}'.format('正在显示所有学生信息'))
        table = PrettyTable(["学号", "姓名", "性别", "分数"])
        if tmp_lst ==None:
            for student in self.lst:
                table.add_row([student.Sid, student.Sname, student.Sex, student.Score])
        else:
            for student in tmp_lst:
                table.add_row([student.Sid, student.Sname, student.Sex, student.Score])
        print(table)

    def updateStudent(self):
        print('{:*^35}'.format('正在更新学生信息'))
        sid = int(input('请输入要更新的学生学号：'))
        i = 0
        for stu in self.lst:
            if stu.Sid == sid:
                print('【请输入要添加的学生信息】')
                score = input('学生分数：')
                self.lst[i].setScore(score)
                print('更新信息成功！')
                return
            i += 1
        print('该学号尚未注册，更新失败')

    def queryStudent(self):
        print('{:*^35}'.format('正在查询学生信息'))
        sid = int(input('请输入要查询的学生学号：'))
        for stu in self.lst:
            if stu.Sid == sid:
                stu.showStudent()
                print('查询信息成功！')
                return
        print('该学号尚未注册，查询失败')


class Menu(DataBase):
    def __init__(self):
        self.lst = []
        self.sid = 171001110 # 设置当前系统的学号开始端

    def welcome(self):
        print('{:^35}'.format('【学生信息管理系统】'))
        print('*' * 40)
        print('1.添加学生信息')
        print('2.删除学生信息')
        print('3.显示所有学生信息')
        print('4.修改学生信息')
        print('5.查询学生信息')
        print('6.保存数据')
        print('7.加载数据')
        print('8.导出数据')
        print('9.导入数据')
        print('0.退出系统')
        print('*' * 40)
        self.ch = int(input('请选择你的操作：'))

    def subQuery(self):
        print('{:^35}'.format('正在查询学生信息'))
        print('*' * 40)
        print('1.按照学号查询到单个学生，并且显示')
        print('2.按照性别查询到多个学生，并且显示')
        print('3.按照姓名查询到学生（可能有多个同名者），并且显示')
        print('4.返回上一层(或者直接回车键）')
        print('*' * 40)
        sub_ch = int(input('请选择你的操作：'))
        subQueryState = {1: self.queryStudent, 2: self.subQueryBySex, 3: self.subQueryByName, 4: self.subBack}
        return subQueryState[sub_ch]()


    def subQueryBySex(self):
        print('{:*^35}'.format('正在查询学生信息'))
        sex = input('请输入要查询的学生性别：')
        success = 0
        tmp_lst= []
        for stu in self.lst:
            if stu.Sex == sex:
                tmp_lst.append(stu)
                success += 1
        if success == 0:
            print('该性别尚未有学生注册！')
        else:
            self.showAllStudent(tmp_lst)
            print('查询信息成功！')

    def subQueryByName(self):
        print('{:*^35}'.format('正在查询学生信息'))
        name = input('请输入要查询的学生姓名：')
        success = 0
        tmp_lst= []
        for stu in self.lst:
            if stu.Sname == name:
                tmp_lst.append(stu)
                success += 1
        if success == 0:
            print('该性别尚未有学生注册！')
        else:
            self.showAllStudent(tmp_lst)
            print('查询信息成功！')

    def subBack(self):
        print('已经返回到主菜单！')

    def getCh(self):
        return self.ch

    def getState(self):
        state = {1: self.insertStudent, 2: self.deleteStudent, 3: self.showAllStudent, 4: self.updateStudent,
                 5: self.subQuery, 6: self.saveData, 7: self.loadData,8:self.toExcel,9:self.readExcel, 0: self.exit}
        return state[self.ch]()

    def toExcel(self):
        name = input("请输入要导出的csv文件名：")
        df = pd.DataFrame(columns=["学号", "姓名", "性别", "分数"])
        for i,stu in enumerate(self.lst):
            df.loc[i] = [stu.Sid,stu.Sname,stu.Sex,stu.Score]
        df.to_csv(name,index=False)
        print('导出信息成功！')
        print('需要退出程序才能生效！')

    def readExcel(self):
        name = input("请输入要导入的csv文件名：")
        df = pd.read_csv(name)
        for line in df.values:
            student = Student(line[0],line[1],line[2],line[3])
            print(student)

            self.lst.append(student)
        self.sid = line[0]+1
        print('导入信息成功！')


    def saveData(self):
        with open('students.pkl', 'wb') as in_data:
            pickle.dump(self.lst, in_data, pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.sid, in_data, pickle.HIGHEST_PROTOCOL)
        print('保存数据成功!')

    def loadData(self):
        with open('students.pkl', 'rb') as out_data:
            self.lst = pickle.load(out_data)
            self.sid = pickle.load(out_data)
        print("加载数据成功!")

    def exit(self):
        sys.exit('谢谢使用，再见！')

    def main(self):
        while True:
            try:
                self.welcome()
                self.getState()
                input('请输入回车键继续。。。')
            except Exception as e:
                print(e)
                print('发现一个错误')


if __name__ == '__main__':
    menu = Menu()
    menu.main()