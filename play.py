# -*- coding: utf-8 -*-
# 程序说明:操作页面
# 创建时间: 2022/1/20 13:53
import time
from tkinter.filedialog import asksaveasfilename, askopenfile
from tkinter.messagebox import askokcancel
from os import system
import pymysql
from pymysql import *
from tkinter.simpledialog import *


class Appp(Frame):
    def __init__(self, master=None, e_return=None):
        super().__init__(master)
        self.master = master
        self.e_return = e_return
        self.pack()
        self.creater()
        self.s_y = False
        self.con = connect(host=self.e_return[0], user=self.e_return[1], password=self.e_return[2],
                           database=self.e_return[3],
                           port=int(self.e_return[4]))
        self.cur = self.con.cursor()
        self.tables = None
        self.table_play()
        master.protocol("WM_DELETE_WINDOW", self.exit_play)
        master.bind("<Control-KeyPress-o>", lambda event:self.open_play())
        master.bind("<Control-KeyPress-s>", lambda event:self.save_play())
        master.bind("<Control-KeyPress-q>", lambda event:self.exit_play())
        master.bind("<Control-KeyPress-p>", lambda event:self.clean_message())
        master.bind("<Control-KeyPress-m>", lambda event: self.modify_play())
        master.bind("<Control-KeyPress-a>", lambda event: self.add_play())
        master.bind("<Control-KeyPress-d>", lambda event: self.delete_play())
        master.bind("<Control-KeyPress-k>", lambda event: self.seek_play())
        master.bind("<Control-KeyPress-r>", lambda event: self.run_play())
        master.bind("<Control-KeyPress-e>", lambda event: self.table_play())
        master.bind("<Control-KeyPress-h>", lambda event: self.help())

    def creater(self):
        # print(self.e_return)
        menubar = Menu(self.master)

        menuFile = Menu(menubar)
        menuEdit = Menu(menubar)
        menuHelp = Menu(menubar)

        menubar.add_cascade(label="文件", menu=menuFile)
        menubar.add_cascade(label="编辑", menu=menuEdit)
        menubar.add_cascade(label="帮助", menu=menuHelp)

        menuFile.add_command(label="打开", accelerator="ctrl+o", command=self.open_play)
        menuFile.add_command(label="保存", accelerator="ctrl+s", command=self.save_play)
        menuFile.add_separator()
        menuFile.add_command(label="退出", accelerator="ctrl+q", command=self.exit_play)

        menuEdit.add_command(label="清除日志", accelerator="ctrl+p", command=self.clean_message)
        menuEdit.add_command(label="刷新", accelerator="ctrl+e", command=self.table_play)

        menuHelp.add_command(label="帮助", accelerator="ctrl+h", command=self.help)
        menuHelp.add_command(label="更新日志", command=self.Change_Log)

        self.master["menu"] = menubar

        self.text1 = Text(self, width=13, height=28)
        self.text1.grid(row=1, column=0, rowspan=6)

        Button(self, text="运行", command=self.run, width=10).grid(row=0, column=0)
        Button(self, text="修改", command=self.modify_play, width=10).grid(row=0, column=1)
        Button(self, text="增加", command=self.add_play, width=10).grid(row=0, column=2)
        Button(self, text="删除", command=self.delete_play, width=10).grid(row=0, column=3)
        Button(self, text="查找", command=self.seek_play, width=10).grid(row=0, column=4)

        self.text2 = Text(self, width=70, height=20)
        self.text2.grid(row=1, column=1, columnspan=4)
        self.scroll1 = Scrollbar(self)
        self.scroll1.config(command=self.text2.yview)
        self.text2.config(yscrollcommand=self.scroll1.set)
        self.scroll1.grid(row=1, column=5, sticky=S + W + E + N)
        # self.scroll1.pack(side=RIGHT, fill=Y)

        self.text3 = Text(self, width=70, height=8, state=DISABLED)
        self.text3.grid(row=2, column=1, columnspan=4)
        self.scroll2 = Scrollbar(self)
        self.scroll2.config(command=self.text3.yview)
        self.text3.config(yscrollcommand=self.scroll2.set)
        self.scroll2.grid(row=2, column=5, sticky=S + W + E + N)
        print(self.e_return)

    def log_messages(self, func):
        try:
            f = open('./log_messages_txt/log_messages.txt', mode='a', encoding='utf-8')
            f.write("执行:")
            f.write(func.__name__)
            f.write('\t')
            f.write("时间:")
            f.write(time.asctime())
            f.write('\t')
            f.write("执行情况:")
            f.write(str(self.isFlag))
        except Exception as e:
            self.text3.insert(END, "\n日志无法更新\n原因：", e)
        finally:
            f.write('\n')
            f.close()

    def add_play(self):
        self.add()
        self.log_messages(self.add)
        self.isFlag = False

    def seek_play(self):
        self.seek()
        self.log_messages(self.seek)
        self.isFlag = False

    def delete_play(self):
        self.delete()
        self.log_messages(self.delete)
        self.isFlag = False

    def exit_play(self):
        self.isFlag = True
        self.log_messages(self.exti)
        self.isFlag = False
        self.exti()

    def table_play(self):
        self.table()
        self.log_messages(self.table)
        self.isFlag = False

    def save_play(self):
        self.save()
        self.log_messages(self.save)
        self.isFlag = False

    def open_play(self):
        self.open()
        self.log_messages(self.open)
        self.isFlag = False

    def modify_play(self):
        self.modify()
        self.log_messages(self.modify)

    def run_play(self):
        self.run()
        self.log_messages(self.run)

    def table(self):
        self.text1.config(state=NORMAL)
        self.text1.delete(0.0, END)
        sql_tabele = "show tables"
        self.cur.execute(sql_tabele)
        v = self.cur.fetchall()
        elements_list = []
        table_list = []
        sql_elements_list = []
        for x in v:
            self.tables = x[0]
            table_list.append(self.tables)
        for table_name in table_list:
            sql_elements = "desc " + table_name
            sql_elements_list.append(sql_elements)
        print(sql_elements_list)
        for sql_run in sql_elements_list:
            self.cur.execute(sql_run)
            v_elements = self.cur.fetchall()
            for i in v_elements:
                elements_list.append(i[0])
            for i in table_list:
                self.text1.insert(END, i + "\n")
                table_list.remove(i)
                for j in elements_list:
                    self.text1.insert(END, "|-" + j + "\n")
                elements_list = []
            print(self.tables)
        self.text1.config(state=DISABLED)
        self.isFlag = True

    def run(self):
        input_type = 0
        counter = 0
        user_input = self.text2.get(INSERT, END)
        user_sql = ""
        parameter_one = 0
        parameter_one_one = 0
        parameter_two = 0
        parameter_two_one = 0
        v = 0

        for i in user_input:
            if i != ";":
                user_sql += i
                counter += 1
                if user_sql == "SELECT " or user_sql == "select ":
                    input_type = 1
                    parameter_one = counter
                if user_sql == "DELETE FROM " or user_sql == "delete from" or user_sql == "TRUNCATE" or user_sql == "truncate":
                    input_type = 2
                if user_sql == "UPDATE " or user_sql == "update ":
                    input_type = 3
                if user_sql == "INSERT INTO " or user_sql == "insert into ":
                    input_type = 4
                if user_sql == "CREATE TABLE " or user_sql == "create table ":
                    input_type = 5
                if user_sql == "ALTER TABLE " or user_sql == "alter table ":
                    input_type = 6
                if user_sql == "DROP TABLE " or user_sql == "drop table ":
                    input_type = 7
                if user_sql[counter-5:counter] == " FROM" or user_sql[counter-5:counter] == " from":
                    print(counter)
                    parameter_one_one = counter-5
                    parameter_two = counter + 1
                if user_sql[counter-1] == " ":
                    parameter_two_one = counter
                    v = 1
                if user_sql[counter-1] != "":
                    v = 0

            elif i == ";":
                user_sql += i
                if user_sql[counter] == ";" and v == 0:
                    parameter_two_one = counter
                break
        parameter_value = user_sql[parameter_one:parameter_one_one]
        parameter_table = user_sql[parameter_two:parameter_two_one]
        print(user_sql + "\n" + str(counter))
        print(parameter_one, parameter_one_one)
        print(parameter_two, parameter_two_one)

        if input_type == 1:
            self.text3.delete(0.0, END)
            if parameter_value != "*":
                parameter_list = list(parameter_value)
                self.text3.config(state=NORMAL)
                try:
                    self.cur.execute(user_sql)
                    c = self.cur.fetchall()
                    self.text3.delete(0.0, END)
                    x = ""
                    for i in range(len(parameter_value) + 1):
                        if i == len(parameter_list) or parameter_list[i] == ",":
                            self.text3.insert(END, x + "\t")
                            x = ""
                        elif parameter_list[i] != ",":
                            x += parameter_list[i]
                    self.text3.insert(END, "\n")
                    for i in c:
                        for w in range(len(i)):
                            print(i[w])
                            self.text3.insert(END, str(i[w]) + "\t")
                        self.text3.insert(END, "\n")
                except pymysql.err.ProgrammingError:
                    self.text3.delete(0.0, END)
                    self.text3.insert(END, "表名错误")
                    self.isFlag = False
                except pymysql.err.OperationalError:
                    self.text3.delete(0.0, END)
                    self.text3.insert(END, "元素名错误")
                    self.isFlag = False
                finally:
                    self.text3.config(state=DISABLED)

            if parameter_value == "*":
                sql1 = "desc" + " " + parameter_table
                self.text3.config(state=NORMAL)
                try:
                    self.cur.execute(sql1)
                    c = self.cur.fetchall()
                    self.text3.delete(0.0, END)
                    for b in c:
                        self.text3.insert(END, b[0] + "\t")
                    self.text3.insert(END, "\n")
                    self.cur.execute(user_sql)
                    x = self.cur.fetchall()
                    for i in x:
                        for mslast in range(len(i)):
                            self.text3.insert(END, str(i[mslast]) + "\t")
                        self.text3.insert(END, "\n")
                    self.isFlag = True
                except pymysql.err.ProgrammingError:
                    self.text3.delete(0.0, END)
                    self.text3.insert(END, "表名错误")
                    self.isFlag = False
                except pymysql.err.OperationalError:
                    self.text3.delete(0.0, END)
                    self.text3.insert(END, "元素名错误")
                    self.isFlag = False
                finally:
                    self.text3.config(state=DISABLED)
        if input_type == 2:
            self.sql_run(user_sql, input_type)
        if input_type == 3:
            self.sql_run(user_sql, input_type)
        if input_type == 4:
            self.sql_run(user_sql, input_type)
        if input_type == 5:
            self.sql_run(user_sql, input_type)
        if input_type == 6:
            self.sql_run(user_sql, input_type)
        if input_type == 7:
            self.sql_run(user_sql, input_type)

    def sql_run(self, sql, number):
        list_yes = ["删除成功", "修改成功", "增加成功", "创建表成功", "表修改成功", "删除表成功"]
        list_error = ["删除失败", "修改失败", "增加失败", "创建表失败", "表修改失败", "删除表失败"]
        number_list = 0
        if number == 2:
            number_list = 0
        if number == 3:
            number_list = 1
        if number == 4:
            number_list = 2
        if number == 5:
            number_list = 3
        if number == 6:
            number_list = 4
        if number == 7:
            number_list = 5
        self.text3.config(state=NORMAL)
        try:
            self.cur.execute(sql)
            self.text3.delete(0.0, END)
            self.text3.insert(END, list_yes[number_list])
            self.con.commit()
            self.isFlag = True
        except pymysql.err.ProgrammingError:
            self.text3.delete(0.0, END)
            self.text3.insert(END,  list_error[number_list] + "\n原因:表名错误")
        except pymysql.err.OperationalError:
            self.text3.delete(0.0, END)
            self.text3.insert(END,  list_error[number_list] + "\n原因:元素名错误")
        finally:
            self.text3.config(state=DISABLED)

    def add(self):
        # x = self.e_return
        # screen = Tk()
        # # self.master.withdraw()
        # AddCmd(master=screen, l_return=x)
        # screen.title("SQL_operation")
        # screen.geometry("600x400")
        # screen.mainloop()
        a = askstring(title="新增", prompt="输入表名", initialvalue=self.tables)
        if a:
            list_add = []
            input_list = []
            sql = "desc" + " " + a
            self.cur.execute(sql)
            c = self.cur.fetchall()
            for b in c:
                list_add.append(b[0])

            for i in range(len(list_add)):
                add_input = askstring(title="值", prompt=list_add[i])
                input_list.append(add_input)
            add_sql = "INSERT INTO " + a + "("
            for i in range(len(list_add)):
                if i == len(list_add) - 1:
                    add_sql += list_add[i]
                else:
                    add_sql += list_add[i] + ","
            add_sql += ") VALUES("
            for i in range(len(list_add)):
                if i == len(input_list) - 1:
                    add_sql += "'" + input_list[i] + "'"
                else:
                    add_sql += "'" + input_list[i] + "'" + ","
            add_sql += ");"
            print(add_sql)
            self.text3.config(state=NORMAL)
            try:
                self.cur.execute(add_sql)
                self.text3.delete(0.0, END)
                self.text3.insert(END, "添加成功")
                self.con.commit()
                self.isFlag = True
            except pymysql.err.DataError:
                self.text3.delete(0.0, END)
                self.text3.insert(END, "添加失败\n原因:没有填写参数")
                self.isFlag = False
            finally:
                self.text3.config(state=DISABLED)

    def delete(self):
        delete_odds = []    # 删除条件列
        delete_value_list = []   # 列中的值
        table_name = askstring(title="删除", prompt="表名", initialvalue=self.tables)

        if table_name:
            delete_type = askinteger(title="删除", prompt="0为清空表中所有数据，1为删除特定数据")
            if delete_type == 1:
                if table_name:
                    delete_number = askinteger(title="删除", prompt="删除的条件数量")
                    for i in range(delete_number):
                        delete_list = askstring(title="删除", prompt="删除列" + str(i + 1))
                        delete_value = askstring(title="删除", prompt="列中的值" + str(i + 1))
                        delete_odds.append(delete_list)
                        delete_value_list.append(delete_value)
                    if delete_number > 1:
                        delete_sentence = askstring(title="逻辑语句", prompt="语句之间的逻辑", initialvalue="AND")
                    delete_sql = "DELETE FROM " + table_name + " WHERE "
                    for i in range(delete_number):
                        if i != delete_number-1:
                            delete_sql += delete_odds[i] + "=" + "'" + delete_value_list[i] + "'" + " " + delete_sentence + " "
                        elif i == delete_number-1:
                            delete_sql += delete_odds[i] + "=" + "'" + delete_value_list[i] + "';"
                    self.text3.config(state=NORMAL)
                    try:
                        self.cur.execute(delete_sql)
                        self.text3.delete(0.0, END)
                        self.text3.insert(END, "已经删除以下元素:\n")
                        for i in delete_odds:
                            self.text3.insert(END, i + "\t")
                        self.text3.insert(END, "\n")
                        for i in delete_value_list:
                            self.text3.insert(END, i + "\t")
                        self.con.commit()
                        self.isFlag = True
                    except pymysql.err.ProgrammingError:
                        self.text3.delete(0.0, END)
                        self.text3.insert(END, "删除错误\n原因:表名错误")
                    except pymysql.err.OperationalError:
                        self.text3.delete(0.0, END)
                        self.text3.insert(END, "删除错误\n原因:元素名错误")
                    finally:
                        self.text3.config(state=DISABLED)
            elif delete_type == 0:
                delete_sql = "TRUNCATE " + table_name
                self.text3.config(state=NORMAL)
                try:
                    self.cur.execute(delete_sql)
                    self.text3.delete(0.0, END)
                    self.text3.insert(END, "已经清空表内所有元素")
                    self.con.commit()
                    self.isFlag = True
                except pymysql.err.ProgrammingError:
                    self.text3.delete(0.0, END)
                    self.text3.insert(END, "删除错误\n原因:表名错误")
                except pymysql.err.OperationalError:
                    self.text3.delete(0.0, END)
                    self.text3.insert(END, "删除错误\n原因:元素名错误")
                finally:
                    self.text3.config(state=DISABLED)

    def seek(self):
        # x = self.e_return
        # screen = Tk()
        # # self.master.withdraw()
        # s = Seekcmd(master=screen, s_return=x)
        # screen.title("SQL_operation")
        # screen.geometry("600x400")
        # screen.mainloop()

        a = askstring(title="查询", prompt="输入表名", initialvalue=self.tables)
        if a:
            b = askstring(title="查询", prompt="元素名")
            if b:

                sql = "SELECT" + " " + b + " " + "FROM" + " " + a
                b_list = list(b)
                print(b_list)
                self.text3.config(state=NORMAL)
                try:
                    if b != "*":
                        self.cur.execute(sql)
                        c = self.cur.fetchall()
                        self.text3.delete(0.0, END)
                        x = ""
                        for i in range(len(b_list) + 1):
                            if i == len(b_list) or b_list[i] == ",":
                                self.text3.insert(END, x + "\t")
                                x = ""
                            elif b_list[i] != ",":
                                x += b_list[i]
                        self.text3.insert(END, "\n")
                        for i in c:
                            for w in range(len(i)):
                                print(i[w])
                                self.text3.insert(END, str(i[w]) + "\t")
                            self.text3.insert(END, "\n")
                    if b == "*":
                        sql1 = "desc" + " " + a
                        self.cur.execute(sql1)
                        c = self.cur.fetchall()
                        self.text3.delete(0.0, END)
                        for b in c:
                            self.text3.insert(END, b[0] + "\t")
                        self.text3.insert(END, "\n")
                        self.cur.execute(sql)
                        x = self.cur.fetchall()
                        for i in x:
                            for mslast in range(len(i)):
                                self.text3.insert(END, str(i[mslast]) + "\t")
                            self.text3.insert(END, "\n")
                    self.isFlag = True
                except pymysql.err.ProgrammingError:
                    self.text3.delete(0.0, END)
                    self.text3.insert(END, "表名错误")
                    self.isFlag = False
                except pymysql.err.OperationalError:
                    self.text3.delete(0.0, END)
                    self.text3.insert(END, "元素名错误")
                    self.isFlag = False
                finally:
                    self.text3.config(state=DISABLED)

                print(a, b)

    def modify(self):
        modify_list = []    # 存放修改的列的名字
        value_list = []     # 存放新值的列表
        odds_list = []      # 存放条件列
        odds_value_list = []    # 存放条件值
        modify_table = askstring(title="修改", prompt="表名", initialvalue=self.tables)
        number = askinteger(title="个数", prompt="修改个数")
        if modify_table and number:
            for i in range(number):
                list_input = askstring(title="列", prompt="修改的列" + str(i+1))
                value_input = askstring(title="值", prompt="修改之后的值" + str(i+1))
                modify_list.append(list_input)
                value_list.append(value_input)
            odds_number = askinteger(title="个数",prompt="条件的个数")
            if odds_number > 1:
                odds_sentence = askstring(title="条件", prompt="条件语句", initialvalue="AND")
            for i in range(odds_number):
                odds_ = askstring(title="条件", prompt="替换的条件")
                odds_value = askstring(title="条件", prompt="替换的条件的原值")
                odds_list.append(odds_)
                odds_value_list.append(odds_value)
            # 组合sql语句
            modify_sql = "UPDATE " + modify_table + " SET "
            for i in range(number):
                if i != number-1:   # 判断是不是最后一个元素
                    modify_sql += modify_list[i] + "=" + "'" + value_list[i] + "'" + ","
                elif i == number-1:
                    modify_sql += modify_list[i] + "=" + "'" + value_list[i] + "'"
            modify_sql += " WHERE "
            for i in range(odds_number):
                if i != odds_number-1 and odds_number > 1:
                    modify_sql += odds_list[i] + "=" + "'" + odds_value_list[i] + "'" + " " + odds_sentence + " "
                elif i == odds_number-1:
                    modify_sql += odds_list[i] + "=" + "'" + odds_value_list[i] + "';"
            # modify_sql += " WHERE " + "'" + odds + "'" + ";"
            print(modify_sql)
            self.text3.config(state=NORMAL)
            try:
                self.cur.execute(modify_sql)
                self.text3.delete(0.0, END)
                self.text3.insert(END, "替换成功")
                self.isFlag = True
                self.con.commit()
            except pymysql.err.OperationalError:
                self.text3.delete(0.0, END)
                self.text3.insert(END, "替换失败\n原因：1.条件错误\n2.列元素错误")
            except pymysql.err.ProgrammingError:
                self.text3.delete(0.0, END)
                self.text3.insert(END, "替换失败\n原因：表名错误")
            finally:
                self.text3.config(state=DISABLED)

    def exti(self):
        s = askokcancel(title="提示", message="是否保存?")
        if s:
            self.save()
        self.cur.close()
        self.con.close()
        self.isFlag = True
        sys.exit()

    def save(self):
        x = self.text2.get(0.0, END)
        filename = asksaveasfilename(title="保存", initialdir="c:", filetypes=[("数据库文件", ".sql")])
        filename_txt = filename + ".db"
        with open(filename_txt, mode='w') as f:
            f.write(x)
        self.isFlag = True

    def open(self):
        s = askokcancel(title="提示", message="是否保存?")
        if s:
            self.save()
        filename = askopenfile(title="选择打开的文件", initialdir="c:", filetypes=[("数据库文件", ".sql")])
        if filename:
            with filename as f:
                self.text2.delete(1.0, END)
                self.text2.insert(INSERT, f.read())

    def clean_message(self):
        with open('./log_messages_txt/log_messages.txt', mode='w') as f:
            f.write("")

    def upload_message(self):
        pass

    def help(self):
        system("help.md")

    def Change_Log(self):
        system("Change_Log.md")


if __name__ == '__main__':
    screen = Tk()
    Appp(master=screen, e_return=('127.0.0.1', 'root', '1234', 'test', '3306'))
    screen.title("SQL_operation")
    screen.geometry("600x400")
    screen.mainloop()
    exit()
