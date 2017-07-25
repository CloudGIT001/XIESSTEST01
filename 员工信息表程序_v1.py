#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:xieshengsen

"""
员工信息表程序，实现增删改查操作：

可进行模糊查询，语法至少支持下面3种:
    select name,age from staff_table where age > 22
    select  * from staff_table where dept = "IT"
    select  * from staff_table where enroll_date like "2013"
查到的信息，打印后，最后面还要显示查到的条数
可创建新员工纪录，以phone做唯一键，staff_id需自增
可删除指定员工信息纪录，输入员工id，即可删除
可修改员工信息，语法如下:
    UPDATE staff_table SET dept="Market" where dept = "IT"
注意：以上需求，要充分使用函数，请尽你的最大限度来减少重复代码
"""

import sqlite3
from prettytable import PrettyTable


# def Sqlite():
#     """
#     使用sqlite3数据库存储员工信息表,
#     :return:
#     """
#     connect = sqlite3.connect("personnel.db")   # 打开一个personnel.db 的数据库，如果不存在，则新建
#     # connect.execute("""create table Employee
#     #             (id INTEGER primary key autoincrement,
#     #             name char(20) not null,
#     #             age int(4) not null,
#     #             phone char(20) not null,
#     #             dept char(20) not null,
#     #             enroll_date char(20) not null);
#     #             """)     # 创建用户表，存储员工信息
#     print ("员工信息表已经打开创建完成")
#     return connect


def AddEmployee(connect):
    """
    新增员工信息函数
    :return:
    """
    flag = True
    while flag:
        print ("请输入创建员工信息[不能为空]~\n")
        id = input("\t请输入员工ID号 或输入 null：")
        if id.strip() == "":
            print ("输入id不能为空，请重新输入~")
            continue

        name = input("\t请输入员工的名字：")
        if name.strip() == "":
            print ("输入名字不能为空，请重新输入~")
            continue

        age = int(input("\t请输入员工的年龄：").strip())

        phone = input("\t请输入员工的电话：")
        if phone.strip() == "":
            print ("输入电话不能为空，请重新输入~")
            continue

        dept = input("\t请输入员工的职业：").strip()
        enroll_date = input("\t请输入员工的入职时间，格式为[2010-12-31]:").strip()

        connect.execute("insert into Employee values (%s,'%s',%s,'%s','%s','%s')"%(id,name,age,phone,dept,enroll_date))
        connect.commit()

        print ("\033[34;1m新员工信息添加完成~\033[0m")
        input("\n按任意键返回主菜单")
        break
    return Main()


def DelEmployee(connect):
    """
    删除员工信息，可根据员工的id 或 姓名来删除
    :return:
    """
    # print ("请选择需要删除的的员工信息，选择 “1”通过ID删除，选择“2”通过姓名删除~")
    flag = True
    while flag:
        input("删除员工操作菜单，按任意键继续：")

        oper_list = PrettyTable(["序号", "选择操作"])
        oper_list.padding_width = 2

        oper_list.add_row([1, "通过ID删除员工信息"])
        oper_list.add_row([2, "通过姓名删除员工信息"])
        oper_list.add_row([3, "返回主菜单"])

        print (oper_list)

        num = input("请输入选择[1 - 3 ]：").strip()
        # if num.isdigit():
        #     num = int(num)

        if num == "1":
            num_id = int(input("请输入需要删除员工的ID号："))
            connect.execute("delete from Employee where id=%d"%num_id)
            connect.commit()
            print ("\033[31;1mID为%d的员工信息删除成功~\033[0m"%num_id)
            input("按任意键继续")


        if num == "2":
            num_name = input("请输入需要删除员工的姓名：")
            connect.execute("delete from Employee where name='%s'"%num_name)
            connect.commit()
            print ("\033[31;1m名字为%s的员工信息删除成功~\033[0m"%num_name)
            input("按任意键继续")

        if num == "3":
            print ("返回主菜单成功")
            flag = False

        # else:
        #     print ("输入有误，请重新输入~")


def CheckEmployee(connect):
    """
    查找员工信息函数，可以选择全部查找，精确查找和模糊查找
    :return:
    """
    flag = False
    while not flag:

        oper_list = PrettyTable(["序号", "选择操作"])
        oper_list.padding_width = 2

        oper_list.add_row([1, "查看全部员工信息"])
        oper_list.add_row([2, "精确查找员工信息"])
        oper_list.add_row([3, "模糊查找员工信息"])
        oper_list.add_row([4, "返回主菜单"])
        print (oper_list)

        # print ("请选择查看模式：“1”查看全部，“2”精确查找，“3”模糊查找，“q\Q”返回主菜单\n")
        num = input("\t请输入选择[1 - 4 ]：").lower()
        # if num.isdigit():
        #     num = int(num)

        if num == "1":
            cursor = connect.execute("select * from Employee")
            oper0 = PrettyTable(["Id", "Name", "Age", "Phone", "Dept", "Enroll_date"])
            for raw in cursor:
                oper0.add_row(raw)
            print (oper0)
            input("按任意键继续")

        if num == "2":
            print ("[a]:id查询，[b]:名字查询，[c]:电话查询")
            choice = input("请输入需要查询的方法：").lower()
            if choice == "a":
                num = int(input("请输入查找的ID："))
                cur1 = connect.execute("select * from Employee where id=%d"%num)
                oper1 = PrettyTable(["Id", "Name", "Age", "Phone", "Dept", "Enroll_date"])
                for i in cur1:
                    oper1.add_row(i)
                print (oper1)
                input("按任意键继续")

            if choice == "b":
                name = input("请输入你需要查询的名字：")
                cur2 = connect.execute("select * from Employee where name='%s'"%name)
                oper2 = PrettyTable(["Id", "Name", "Age", "Phone", "Dept", "Enroll_date"])
                for j in cur2:
                    oper2.add_row(j)
                print(oper2)
                input("按任意键继续")

            if choice == "c":
                phone = input("请输入你需要查询的电话：")
                cur3 = connect.execute("select * from Employee where phone='%s'" %phone)
                oper3 = PrettyTable(["Id", "Name", "Age", "Phone", "Dept", "Enroll_date"])
                for k in cur3:
                    oper3.add_row(k)
                print (oper3)
                input("按任意键继续")

            # if choice != "a" or choice != "b" or choice != "c":
            #     print ("任意键继续")

        if num == "3":
            print ("[A]:部门查找，[B]:年龄查找，[C]:入职时间查找")
            choice1 = input("请输入需要查询的方法：").upper()
            if choice1 == "A":
                dept = input("请输入你需要查询的部门：").lower()
                cur4 = connect.execute("select * from Employee where dept='%s'" %dept)
                oper4 = PrettyTable(["Id", "Name", "Age", "Phone", "Dept", "Enroll_date"])
                for x in cur4:
                    oper4.add_row(x)
                print (oper4)
                input("按任意键继续")

            if choice1 == "B":
                age = input("请输入你需要查询的年龄范围[例：>20]：")
                cur5 = connect.execute("select * from Employee where age%s" %age)
                oper5 = PrettyTable(["Id", "Name", "Age", "Phone", "Dept", "Enroll_date"])
                for y in cur5:
                    oper5.add_row(y)
                print(oper5)
                input("按任意键继续")

            if choice1 == "C":
                enroll_date = input("请输入你需要查询的年份[例：2016%]：")
                cur6 = connect.execute("select * from Employee where Enroll_date like '%s'" %enroll_date)
                oper6 = PrettyTable(["Id", "Name", "Age", "Phone", "Dept", "Enroll_date"])
                for z in cur6:
                    oper6.add_row(z)
                print(oper6)
                input("按任意键继续")

        if num == "4":
            print ("成功返回主菜单")
            return Main()

        # else:
        #     print ("\033[31;1m输入有误，请重新输入~\033[0m")



def MdifyEmployee(connect):
    """
    员工信息函数，修改员工信息
    :return:
    """
    flag = True
    while flag:

        open_list = PrettyTable(["序号","选择操作"])
        open_list.padding_width = 2
        open_list.add_row([1, "修改员工姓名"])
        open_list.add_row([2, "修改员工年龄"])
        open_list.add_row([3, "修改员工电话"])
        open_list.add_row([4, "修改员工部门"])
        open_list.add_row([5, "修改员工入职时间"])
        open_list.add_row([6, "返回主菜单"])

        print ("修改操作\n",open_list)

        # # name_list = []
        # Name = connect.execute("select name from Employee")
        # # for m in Name:
        # #     name_list.append(m)
        # # print (name_list)

        choice2 = input("请选择需要修改的信息：")

        if choice2 == "1":
            name1 = input("请输入需要修改的员工姓名：")
            # name1 = tuple(name1,)
            # # print (name1)

            # if name1 in name_list:

            name2 = input("请输入修改后员工的姓名：")
            connect.execute("update Employee set name='%s' where name='%s'"%(name2,name1))
            connect.commit()
            print("员工姓名已经修改完成")
            cour1 = connect.execute("select * from Employee where name='%s'" % name2)
            oper1 = PrettyTable(["Id", "Name", "Age", "Phone", "Dept", "Enroll_date"])
            for i in cour1:
                oper1.add_row(i)
            print(oper1)

        if choice2 == "2":
            name3 = input("请输入需要修改的员工姓名：")
            age1 = int(input("请输入修改员工的年龄："))
            connect.execute("update Employee set age=%d where name='%s'"%(age1,name3))
            connect.commit()
            print("员工年龄已经修改完成")
            cour2 = connect.execute("select * from Employee where name='%s'" % name3)
            oper2 = PrettyTable(["Id", "Name", "Age", "Phone", "Dept", "Enroll_date"])
            for j in cour2:
                oper2.add_row(j)
            print (oper2)

        if choice2 == "3":
            name4 = input("请输入需要修改的员工姓名：")
            phone1 = input("请输入修改员工的电话：")
            connect.execute("update Employee set phone='%s' where name='%s'" % (phone1, name4))
            connect.commit()
            print("员工的电话已经修改完成")
            cour3 = connect.execute("select * from Employee where name='%s'" % name4)
            oper3 = PrettyTable(["Id", "Name", "Age", "Phone", "Dept", "Enroll_date"])
            for k in cour3:
                oper3.add_row(k)
            print (oper3)

        if choice2 == "4":
            name5 = input("请输入需要修改的员工姓名：")
            dept1 = input("请输入修改员工的部门：").upper()
            connect.execute("update Employee set dept='%s' where name='%s'" % (dept1, name5))
            connect.commit()
            print("员工年龄已经修改完成")
            cour4 = connect.execute("select * from Employee where name='%s'" % name5)
            oper4 = PrettyTable(["Id", "Name", "Age", "Phone", "Dept", "Enroll_date"])
            for l in cour4:
                oper4.add_row(l)
            print (oper4)

        if choice2 == "5":
            name6 = input("请输入需要修改的员工姓名：")
            date1 = input("请输入修改员工的入职时间[例：2017-01-01]：")
            connect.execute("update Employee set Enroll_date='%s' where name='%s'" % (date1, name6))
            connect.commit()
            print("员工入职时间已经修改完成")
            cour5 = connect.execute("select * from Employee where name='%s'" % name6)
            oper5 = PrettyTable(["Id", "Name", "Age", "Phone", "Dept", "Enroll_date"])
            for n in cour5:
                oper5.add_row(n)
            print(oper5)

        if choice2 == "6":
            print ("返回主菜单成功~")
            return Main()

        else:
            print ("输入错误，请重新输入")
            continue


def Main():
    """
    主逻辑函数
    :return:
    """
    connect = sqlite3.connect("personnel.db")
    print("\n员工信息表已经打开创建完成\n")

    operation = {"1": ["创建员工", AddEmployee],
                 "2": ["删除员工", DelEmployee],
                 "3": ["查找员工", CheckEmployee],
                 "4": ["修改员工信息", MdifyEmployee],
                 # "5": ["退出", Quit]
                 }
    oper_list = PrettyTable(["序号","内容"])
    oper_list.padding_width = 2
    oper_list.add_row([1, operation["1"][0]])
    oper_list.add_row([2, operation["2"][0]])
    oper_list.add_row([3, operation["3"][0]])
    oper_list.add_row([4, operation["4"][0]])
    oper_list.add_row([5, "退出程序"])

    # result = Sqlite()

    flag = True
    while flag:
        print ("主菜单操作\n",oper_list)
        action_oper = input("请选择你的操作:").strip()

        # connect = sqlite3.connect("personnel.db")
        # print("员工信息表已经打开创建完成\n")

        if action_oper == "1":     # 新增员工信息，调用AddEmployee()函数
            AddEmployee(connect)

        if action_oper == "2":
            DelEmployee(connect)

        if action_oper == "3":
            CheckEmployee(connect)

        if action_oper == "4":
            MdifyEmployee(connect)


        elif action_oper == "5":
            flag = False
            # return action_oper

        # else:
        #     print("\033[31;1m输入有误，请重新输入[1-5]的整数\033[0m")
        #     continue
        #
        # else:
        #     operation[action_oper][1](




if __name__ == "__main__":
    Main()