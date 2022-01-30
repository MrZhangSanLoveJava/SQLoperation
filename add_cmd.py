# -*- coding: utf-8 -*-
# 程序说明:
# 创建时间: 2022/1/24 16:53
from tkinter import *
from tkinter.font import *


class AddCmd(Frame):
    def __init__(self, master=None, l_return=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.creatter()

    def creatter(self):
        text1 = Font(size=60)
        Label(self, text="添加元素", fg="mediumSpringGreen", bg="yellow", font=text1).grid(row=0, column=0, columnspan=5, rowspan=3)
        Label(self, text="表名", font=text1).grid(row=3, column=0)
        self.entry1 = Entry(self)
        self.entry1.grid(row=3, column=1)
        Label(self, text="添加名字", font=text1).grid(row=4, column=0)
        self.entry2 = Entry(self)
        self.entry2.grid(row=4, column=1)
        Button(self, text="确定", command=self.yes).grid(row=5, column=0)
        Button(self, text="取消", command=self.no).grid(row=5, column=1)

    def yes(self):
        x = self.entry1.get()
        y = self.entry2.get()
        # try:
        #     sql = """insert into t_student(sname, age, score) values(%s,%s,%s,%s)"""

    def no(self):
        pass
