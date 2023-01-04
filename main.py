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
        self.kosdaq_btn_search.clicked.connect(self.search)
        self.covering_btn_search.clicked.connect(self.search)
        self.btn_go_manage.clicked.connect(self.go_manage)
        self.btn_go_search.clicked.connect(self.go_search)
        self.btn_search_to_main.clicked.connect(self.go_main)
        self.btn_manage_to_main.clicked.connect(self.go_main)
        self.covering_date_before.dateChanged.connect(self.set_date)
        self.covering_date_after.dateChanged.connect(self.set_date)
        self.kosdaq_date_before.dateChanged.connect(self.set_date)
        self.kosdaq_date_after.dateChanged.connect(self.set_date)
        self.kosdaq_date_add.dateChanged.connect(self.set_groupbox)
        self.covering_date_add.dateChanged.connect(self.set_groupbox)
        self.tab_search.currentChanged.connect(self.set_search_tab)
        self.kosdaq_label_impossible.setVisible(False)
        self.covering_label_impossible.setVisible(False)

    def go_main(self):
        self.stackedWidget.setCurrentWidget(self.stack_main)

    def go_manage(self):
        self.stackedWidget.setCurrentWidget(self.stack_manage)

    def go_search(self):
        self.stackedWidget.setCurrentWidget(self.stack_search)

    def set_search_tab(self):
        print(self.tab_search.currentIndex())
        self.covering_table.setRowCount(0)
        self.kosdaq_table_search.setRowCount(0)

    def set_date(self):
        if self.covering_date_before.date() > self.covering_date_after.date():
            self.covering_date_after.setDate(self.covering_date_before.date())
            self.covering_lable_impossible.setVisible(True)
        else:
            self.covering_lable_impossible.setVisible(False)

        if self.kosdaq_date_before.date() > self.kosdaq_date_after.date():
            self.kosdaq_date_after.setDate(self.kosdaq_date_before.date())
            self.kosdaq_lable_impossible.setVisible(True)
        else:
            self.kosdaq_lable_impossible.setVisible(False)

    def set_groupbox(self):
        date_send = self.sender()
        date_str = date_send.date().toString('yyyy-MM-dd')
        weekday = date_send.date().dayOfWeek()
        possible = True
        table = None
        date_label = None
        group = None

        if date_send == self.kosdaq_date_add:
            table = 'kosdaq'
            date_label = self.kosdaq_label_add
            group = self.kosdaq_group_add
            # sql = "SELECT * FROM kosdaq WHERE 날짜 = '" + date_str + "'"
        if date_send == self.covering_date_add:
            table = 'covering'
            date_label = self.covering_label_add
            group = self.covering_group_add
            # sql = "SELECT * FROM covering WHERE 날짜 = '" + date_str + "'"
        sql = "SELECT * FROM " + table + " WHERE 날짜 = '" + date_str + "'"
        print(sql)

        if weekday == 6 or weekday == 7:
            print("주말")
            possible = False
        print(possible)

        if possible:
            con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
            cur = con.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            for i in rows:
                if date_str == i[0]:
                    date_label.setText("해당 날짜에 이미 데이터가 존재함")
                    print("데이터 존재")
                    possible = False
                    group.setEnabled(False)
                    break
            if possible:
                date_label.setText('')
                group.setEnabled(True)
            con.close()
        else:
            date_label.setText("주말 선택 불가")
            group.setEnabled(False)

    def csearch(self):
        self.covering_lable_impossible.setVisible(False)
        self.covering_table.setRowCount(0)
        date_str1 = self.covering_date_before.date().toString('yyyy-MM-dd')
        date_str2 = self.covering_date_after.date().toString('yyyy-MM-dd')
        print(date_str1, date_str2)
        sql = "SELECT * FROM covering WHERE 날짜 >= '" + date_str1 + "' and 날짜 <= '" + date_str2 + "'"

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

    def search(self):
        self.kosdaq_lable_impossible.setVisible(False)
        self.kosdaq_table.setRowCount(0)
        date_str1 = self.kosdaq_date_before.date().toString('yyyy-MM-dd')
        date_str2 = self.kosdaq_date_after.date().toString('yyyy-MM-dd')
        print(date_str1, date_str2)
        sql = "SELECT * FROM covering WHERE 날짜 >= '" + date_str1 + "' and 날짜 <= '" + date_str2 + "'"

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
