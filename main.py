import pymysql
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

form_class = uic.loadUiType("main.ui")[0]

host_str = '10.10.21.116'
user_str = 'stock_admin'
password_str = 'admin1234'


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.stackedWidget.setCurrentWidget(self.stack_main)
        self.kosdaq_label_impossible.setVisible(False)
        self.covering_label_impossible.setVisible(False)

        self.kosdaq_date_add.setDate(QDate.currentDate())
        self.kosdaq_date_del.setDate(QDate.currentDate())
        self.kosdaq_date_edit.setDate(QDate.currentDate())
        self.covering_date_add.setDate(QDate.currentDate())
        self.covering_date_del.setDate(QDate.currentDate())
        self.covering_date_edit.setDate(QDate.currentDate())
        self.kosdaq_date_add.setMaximumDate(QDate.currentDate())
        self.kosdaq_date_del.setMaximumDate(QDate.currentDate())
        self.kosdaq_date_edit.setMaximumDate(QDate.currentDate())
        self.covering_date_add.setMaximumDate(QDate.currentDate())
        self.covering_date_del.setMaximumDate(QDate.currentDate())
        self.covering_date_edit.setMaximumDate(QDate.currentDate())
        # self.set_date_minimum()
        self.kosdaq_date_after.setMaximumDate(QDate.currentDate())
        self.covering_date_after.setMaximumDate(QDate.currentDate())

        self.btn_go_manage.clicked.connect(self.go_manage)
        self.btn_go_search.clicked.connect(self.go_search)
        self.btn_search_to_main.clicked.connect(self.go_main)
        self.btn_manage_to_main.clicked.connect(self.go_main)
        self.kosdaq_btn_search.clicked.connect(self.kosdaq_search)
        self.covering_btn_search.clicked.connect(self.covering_search)
        self.kosdaq_btn_addDate.clicked.connect(self.set_group)
        self.kosdaq_btn_delDate.clicked.connect(self.set_group)
        self.kosdaq_btn_editDate.clicked.connect(self.set_group)
        self.covering_btn_addDate.clicked.connect(self.set_group)
        self.covering_btn_delDate.clicked.connect(self.set_group)
        self.covering_btn_editDate.clicked.connect(self.set_group)

        self.kosdaq_date_before.dateChanged.connect(self.set_date)
        self.kosdaq_date_after.dateChanged.connect(self.set_date)
        self.covering_date_before.dateChanged.connect(self.set_date)
        self.covering_date_after.dateChanged.connect(self.set_date)
        self.kosdaq_date_add.dateChanged.connect(self.set_add_button)
        self.covering_date_add.dateChanged.connect(self.set_add_button)
        self.kosdaq_date_del.dateChanged.connect(self.set_del_edit_button)
        self.covering_date_del.dateChanged.connect(self.set_del_edit_button)
        self.kosdaq_date_edit.dateChanged.connect(self.set_del_edit_button)
        self.covering_date_edit.dateChanged.connect(self.set_del_edit_button)

        self.tab_search.currentChanged.connect(self.reset_tab)
        self.tab_manage.currentChanged.connect(self.reset_tab)
        self.kosdaq_tab_manage.currentChanged.connect(self.reset_tab)
        self.covering_tab_manage.currentChanged.connect(self.reset_tab)

    # def set_date_minimum(self):
    #     self.kosdaq_date_before.setMinimumDate()


    def go_main(self):
        self.stackedWidget.setCurrentWidget(self.stack_main)

    def go_manage(self):
        self.stackedWidget.setCurrentWidget(self.stack_manage)

    def go_search(self):
        self.stackedWidget.setCurrentWidget(self.stack_search)

    def reset_tab(self):
        self.covering_table.setRowCount(0)
        self.kosdaq_table.setRowCount(0)

        self.kosdaq_label_del1.setText('')
        self.kosdaq_label_del2.setText('')
        self.kosdaq_label_del3.setText('')
        self.kosdaq_label_del4.setText('')
        self.kosdaq_label_del5.setText('')
        self.kosdaq_label_del6.setText('')

        self.covering_label_del1.setText('')
        self.covering_label_del2.setText('')
        self.covering_label_del3.setText('')
        self.covering_label_del4.setText('')
        self.covering_label_del5.setText('')
        self.covering_label_del6.setText('')

        self.kosdaq_label_edit1.setText('')
        self.kosdaq_label_edit2.setText('')
        self.kosdaq_label_edit3.setText('')
        self.kosdaq_label_edit4.setText('')
        self.kosdaq_label_edit5.setText('')
        self.kosdaq_label_edit6.setText('')

        self.covering_label_edit1.setText('')
        self.covering_label_edit2.setText('')
        self.covering_label_edit3.setText('')
        self.covering_label_edit4.setText('')
        self.covering_label_edit5.setText('')
        self.covering_label_edit6.setText('')

    def set_date(self):
        if self.covering_date_before.date() > self.covering_date_after.date():
            self.covering_date_after.setDate(self.covering_date_before.date())
            self.covering_label_impossible.setVisible(True)
        else:
            self.covering_label_impossible.setVisible(False)

        if self.kosdaq_date_before.date() > self.kosdaq_date_after.date():
            self.kosdaq_date_after.setDate(self.kosdaq_date_before.date())
            self.kosdaq_label_impossible.setVisible(True)
        else:
            self.kosdaq_label_impossible.setVisible(False)

    def set_add_button(self):
        date_send = self.sender()
        date_str = date_send.date().toString('yyyy-MM-dd')
        weekday = date_send.date().dayOfWeek()
        possible = True
        table = None
        date_label = None
        btn = None

        if date_send == self.kosdaq_date_add:
            self.kosdaq_group_add.setEnabled(False)
            table = 'kosdaq'
            date_label = self.kosdaq_label_add
            btn = self.kosdaq_btn_addDate
        if date_send == self.covering_date_add:
            self.covering_group_add.setEnabled(False)
            table = 'covering'
            date_label = self.covering_label_add
            btn = self.covering_btn_addDate

        sql = f"SELECT * FROM {table} WHERE 날짜 = '{date_str}'"
        print(sql)

        if weekday == 6 or weekday == 7:
            print("주말")
            possible = False

        if possible:
            con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
            with con:
                with con.cursor() as cur:
                    cur.execute(sql)
                    result = cur.fetchall()
                    if len(result) != 0:
                        print("추가 - 데이터 존재")
                        date_label.setText("해당 날짜에 이미 데이터가 존재함")
                        btn.setEnabled(False)
                    else:
                        date_label.setText("데이터 추가 가능")
                        btn.setEnabled(True)
        else:
            date_label.setText("주말 선택 불가")
            btn.setEnabled(False)

    def set_del_edit_button(self):
        date_send = self.sender()
        date_str = date_send.date().toString('yyyy-MM-dd')
        weekday = date_send.date().dayOfWeek()
        possible = True
        table = None
        date_label = None
        btn = None
        set_text = None

        if date_send == self.kosdaq_date_del:
            self.kosdaq_group_del.setEnabled(False)
            table = 'kosdaq'
            date_label = self.kosdaq_label_del
            btn = self.kosdaq_btn_delDate
            set_text = '삭제'
        if date_send == self.covering_date_del:
            self.covering_group_del.setEnabled(False)
            table = 'covering'
            date_label = self.covering_label_del
            btn = self.covering_btn_delDate
            set_text = '삭제'
        if date_send == self.kosdaq_date_edit:
            self.kosdaq_group_edit.setEnabled(False)
            table = 'kosdaq'
            date_label = self.kosdaq_label_edit
            btn = self.kosdaq_btn_editDate
            set_text = '수정'
        if date_send == self.covering_date_edit:
            self.covering_group_edit.setEnabled(False)
            table = 'covering'
            date_label = self.covering_label_edit
            btn = self.covering_btn_editDate
            set_text = '수정'

        sql = f"SELECT * FROM {table} WHERE 날짜 = '{date_str}'"
        print(sql)

        if weekday == 6 or weekday == 7:
            print("주말")
            possible = False
        print(possible)

        if possible:
            con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
            with con:
                with con.cursor() as cur:
                    cur.execute(sql)
                    result = cur.fetchall()
                    if len(result) != 0:
                        print(f"{set_text} - 데이터 존재")
                        date_label.setText(f"데이터 {set_text} 가능")
                        btn.setEnabled(True)
                    else:
                        date_label.setText(f"{set_text}할 데이터가 없음")
                        print("데이터 없음")
                        btn.setEnabled(False)
        else:
            date_label.setText("주말 선택 불가")
            btn.setEnabled(False)

    def set_group(self):
        date_send = self.sender()

        if date_send == self.kosdaq_btn_addDate:
            self.kosdaq_group_add.setEnabled(True)
        if date_send == self.covering_btn_addDate:
            self.covering_group_add.setEnabled(True)

        if date_send == self.kosdaq_btn_delDate or date_send == self.covering_btn_delDate \
                or date_send == self.kosdaq_btn_editDate or date_send == self.covering_btn_editDate:
            group = None
            table = None
            date_info = None
            label_list = list()

            if date_send == self.kosdaq_btn_delDate:
                group = self.kosdaq_group_del
                date_info = self.kosdaq_date_del
                label_list = [self.kosdaq_label_del1, self.kosdaq_label_del2, self.kosdaq_label_del3,
                              self.kosdaq_label_del4, self.kosdaq_label_del5, self.kosdaq_label_del6]
                table = 'kosdaq'
            if date_send == self.covering_btn_delDate:
                group = self.covering_group_del
                date_info = self.covering_date_del
                label_list = [self.covering_label_del1, self.covering_label_del2, self.covering_label_del3,
                              self.covering_label_del4, self.covering_label_del5, self.covering_label_del6]
                table = 'covering'
            if date_send == self.kosdaq_btn_editDate:
                group = self.kosdaq_group_edit
                date_info = self.kosdaq_date_edit
                label_list = [self.kosdaq_label_edit1, self.kosdaq_label_edit2, self.kosdaq_label_edit3,
                              self.kosdaq_label_edit4, self.kosdaq_label_edit5, self.kosdaq_label_edit6]
                table = 'kosdaq'
            if date_send == self.covering_btn_editDate:
                group = self.covering_group_edit
                date_info = self.covering_date_edit
                label_list = [self.covering_label_edit1, self.covering_label_edit2, self.covering_label_edit3,
                              self.covering_label_edit4, self.covering_label_edit5, self.covering_label_edit6]
                table = 'covering'

            group.setEnabled(True)
            date_str = date_info.date().toString('yyyy-MM-dd')
            sql = f"SELECT * FROM {table} WHERE 날짜 = '{date_str}'"
            print(sql)

            con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
            cur = con.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            for i in rows:
                for j in range(1, 7):
                    label_list[j-1].setText(str(i[j]))
            con.close()


    def covering_search(self):
        self.covering_label_impossible.setVisible(False)
        self.covering_table.setRowCount(0)
        date_str1 = self.covering_date_before.date().toString('yyyy-MM-dd')
        date_str2 = self.covering_date_after.date().toString('yyyy-MM-dd')
        print(date_str1, date_str2)
        sql = f"SELECT * FROM covering WHERE 날짜 >= '{date_str1}' and 날짜 <= '{date_str2}'"

        print(sql)

        con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        row = 0
        col = 0
        self.covering_table.setRowCount(len(rows))
        for i in rows:
            for j in i:
                print(j, end='  ')
                self.covering_table.setItem(col, row, QTableWidgetItem(str(j)))
                row += 1
            row = 0
            col += 1
            print()

        con.close()

    def kosdaq_search(self):
        print("ksearch")
        self.kosdaq_label_impossible.setVisible(False)
        self.kosdaq_table.setRowCount(0)
        date_str1 = self.kosdaq_date_before.date().toString('yyyy-MM-dd')
        date_str2 = self.kosdaq_date_after.date().toString('yyyy-MM-dd')
        print(date_str1, date_str2)
        sql = f"SELECT * FROM covering WHERE 날짜 >= '{date_str1}' and 날짜 <= '{date_str2}'"

        print(sql)

        con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        row = 0
        col = 0
        self.kosdaq_table.setRowCount(len(rows))
        for i in rows:
            for j in i:
                print(j, end='  ')
                self.kosdaq_table.setItem(col, row, QTableWidgetItem(str(j)))
                row += 1
            row = 0
            col += 1
            print()

        con.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
