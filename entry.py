# -*- coding: utf-8 -*-
# 程序说明:
# 创建时间: 2022/1/19 23:44
from tkinter import *
from tkinter.font import *

import pymysql
from pymysql import *

from play import Appp


class App(Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.pack()
        self.creater()
        self.entry1 = None
        self.entry2 = None
        self.entry3 = None
        self.entry4 = None
        self.entry5 = None
        self.isFlag = False

    def creater(self):
        text1 = Font(size=40)
        font1 = Font(size=20)
        self.v1 = StringVar()
        self.v2 = StringVar()
        self.v3 = StringVar()
        self.v4 = StringVar()
        self.v5 = StringVar()
        Label(self, text="MySQL可视化操作", bg='gold', fg='cyan', font=text1).grid(row=0, column=0, columnspan=6)
        Label(self, text="数据库的地址", font=font1).grid(row=1, column=2)
        self.entry1 = Entry(self, textvariable=self.v1)
        self.entry1.grid(row=1, column=3)
        self.v1.set("127.0.0.1")
        Label(self, text="数据库用户名", font=font1).grid(row=2, column=2)
        self.entry2 = Entry(self, textvariable=self.v2)
        self.entry2.grid(row=2, column=3)
        Label(self, text="数据库的密码", font=font1).grid(row=3, column=2)
        self.entry3 = Entry(self, textvariable=self.v3)
        self.entry3.grid(row=3, column=3)
        Label(self, text="数据库的名字", font=font1).grid(row=4, column=2)
        self.entry4 = Entry(self, textvariable=self.v4)
        self.entry4.grid(row=4, column=3)
        Label(self, text="数据库的端口号", font=font1).grid(row=5, column=2)
        self.entry5 = Entry(self, textvariable=self.v5)
        self.entry5.grid(row=5, column=3)
        self.v5.set(3306)
        Button(self, text="确定", command=self.yes, width=10, height=2).grid(row=6, column=1)
        Button(self, text="重置", command=self.resetting, width=10, height=2).grid(row=6, column=2)
        Button(self, text="测试连接", command=self.test, width=10, height=2).grid(row=6, column=3)
        Button(self, text="退出", command=self.out, width=10, height=2).grid(row=6, column=4)
        self.text1 = Text(self, height=9)
        self.text1.grid(row=7, column=0, columnspan=6)
        self.text1.config(state=NORMAL)
        self.text1.insert(0.0, "欢迎使用MySQL可视化查询软件\n版本:v1.0.0")
        self.text1.config(state=DISABLED)

    def yes(self):
        if self.isFlag:
            x = (self.v1.get(), self.v2.get(), self.v3.get(), self.v4.get(), self.v5.get())
            screen = Tk()
            self.master.withdraw()
            Appp(master=screen, e_return=x)
            screen.title("SQL_operation")
            # screen.iconphoto(False, PhotoImage(file="./ico/tubiao.png"))
            screen.geometry("600x400")
            self.master.quit()
            screen.mainloop()
            sys.exit()
        elif not self.isFlag:
            self.text1.config(state=NORMAL)
            self.text1.delete(0.0, END)
            self.text1.insert(0.0, "请测试连接后再点确定")
            self.text1.config(state=DISABLED)

    def resetting(self):
        self.v1.set("127.0.0.1")
        self.v2.set("")
        self.v3.set("")
        self.v4.set("")
        self.v5.set(3306)
        self.text1.config(state=NORMAL)
        self.text1.delete(0.0, END)
        self.text1.insert(0.0, "欢迎使用MySQL可视化查询软件\n版本:v1.0.0")
        self.text1.config(state=DISABLED)
        self.isFlag = False

    def test(self):
        self.text1.config(state=NORMAL)
        try:
            connect(host=self.v1.get(), user=self.v2.get(), password=self.v3.get(), database=self.v4.get(),
                    port=int(self.v5.get()))
        except pymysql.err.OperationalError:
            self.text1.delete(0.0, END)
            self.text1.insert(0.0, "连接失败\n错误原因:未知错误\n解决方法：1、检查数据库地址是否正确\n2、检查用户名是否正确\n3、检查端口号是否正确"
                                   "\n4、检查数据库名是否正确\n5、数据库可能没有开启")
        except RuntimeError:
            self.text1.delete(0.0, END)
            self.text1.insert(0.0, "连接失败\n错误原因:用户名错误")
        except TypeError:
            self.text1.delete(0.0, END)
            self.text1.insert(0.0, "连接失败\n错误原因:端口类型错误")
        except ValueError:
            self.text1.delete(0.0, END)
            self.text1.insert(0.0, "连接失败\n错误原因:未填写完毕")
        else:
            self.text1.delete(0.0, END)
            self.text1.insert(0.0, "测试成功")
            self.isFlag = True
        finally:
            self.text1.config(state=DISABLED)

    def out(self):
        sys.exit()


root = Tk()
root.geometry("600x400")
root.iconphoto(True, PhotoImage(file="./ico/tubiao.png"))
root.title("SQL_operation v1.0.0")
app = App(master=root)
root.mainloop()
exit()
