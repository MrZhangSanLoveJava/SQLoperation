# -*- coding: utf-8 -*-
# 程序说明:
# 创建时间: 2022/1/25 15:35
from tkinter import *
from tkinter.font import *
from pymysql import *


class Seekcmd(Frame):
    def __init__(self, master=None, s_return=None):
        super().__init__(master)
        self.master = master
        self.s_return = s_return
        self.pack()
        self.creater()
        self.success = None
        self.element = None
        self.content = None
        self.s_y = True
        self.x = False

    def creater(self):
        text1 = Font(size=60)
        Label(self, text="查询元素", fg="mediumSpringGreen", bg="yellow", font=text1).grid(row=0, column=0, columnspan=5,
                                                                                       rowspan=3)
        Label(self, text="表名", font=text1).grid(row=3, column=0)
        self.entry1 = Entry(self)
        self.entry1.grid(row=3, column=1)
        Label(self, text="元素名", font=text1).grid(row=4, column=0)
        self.entry2 = Entry(self)
        self.entry2.grid(row=4, column=1)
        Button(self, text="确定", command=self.yes).grid(row=5, column=0)
        Button(self, text="取消", command=self.no).grid(row=5, column=1)

    def yes(self):
        x = self.entry1.get()
        y = self.entry2.get()
        con = connect(host=self.s_return[0], user=self.s_return[1], password=self.s_return[2], database=self.s_return[3],
                port=int(self.s_return[4]))
        cur = con.cursor()
        sql = "SELECT" + " " + y + " " + "FROM" + " " + x
        try:
            cur.execute(sql)
            c = cur.fetchall()
            self.success = True
            self.element = y
            self.content = c
            print(type(sql))
            # return (1, y, c)
        except Exception as e:
            # return (0, e)
            self.y = e
            self.success = False
            # print("ss")
        finally:
            cur.close()
            con.close()
        self.master.withdraw()
        self.exit()
        return self.element, self.content

    def no(self):
        self.master.withdraw()
        self.exit()

    def exit(self):
        self.quit()