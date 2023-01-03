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
        self.btn_csearch.clicked.connect(self.csearch)
        self.btn_ksearch.clicked.connect(self.ksearch)
        self.btn_gomanage.clicked.connect(self.go_manage)
        self.btn_gosearch.clicked.connect(self.go_search)
        self.btn_sgomain.clicked.connect(self.go_main)
        self.btn_mgomain.clicked.connect(self.go_main)
        self.date_cbefore.dateChanged.connect(self.set_date)
        self.date_cafter.dateChanged.connect(self.set_date)
        self.date_kbefore.dateChanged.connect(self.set_date)
        self.date_kafter.dateChanged.connect(self.set_date)
        self.date_kadd.dateChanged.connect(self.set_groupbox)
        # self.date_cadd.dateChanged.connect(self.set_groupbox)
        self.tab_search.currentChanged.connect(self.set_searchtab)
        self.label_kimpo.setVisible(False)
        self.label_cimpo.setVisible(False)

    def go_main(self):
        self.stackedWidget.setCurrentWidget(self.stack_main)

    def go_manage(self):
        self.stackedWidget.setCurrentWidget(self.stack_manage)

    def go_search(self):
        self.stackedWidget.setCurrentWidget(self.stack_search)

    def set_searchtab(self):
        print(self.tab_search.currentIndex())
        self.table_csearch.setRowCount(0)
        self.table_ksearch.setRowCount(0)

    def set_date(self):
        if self.date_cbefore.date() > self.date_cafter.date():
            self.date_cafter.setDate(self.date_cbefore.date())
            self.label_cimpo.setVisible(True)
        else:
            self.label_cimpo.setVisible(False)

        if self.date_kbefore.date() > self.date_kafter.date():
            self.date_kafter.setDate(self.date_kbefore.date())
            self.label_kimpo.setVisible(True)
        else:
            self.label_kimpo.setVisible(False)

    def set_groupbox(self):
        date_str = self.date_kadd.date().toString('yyyy-MM-dd')
        sql = ''
        date_send = self.sender()
        print(date_send)
        print(self.date_kadd)
        if date_send == self.date_kadd:
            sql = "SELECT * FROM kosdaq WHERE 날짜 >= '" + date_str + "'"
        # if date_send == self.date_cadd:
        #     sql = "SELECT * FROM covering WHERE 날짜 >= '" + date_str + "'"

        con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for i in rows:
            if date_str == i[0]:
                print("ㄴㄴ")
                break
        con.close()

    def csearch(self):
        self.label_cimpo.setVisible(False)
        self.table_csearch.setRowCount(0)
        date_str1 = self.date_cbefore.date().toString('yyyy-MM-dd')
        date_str2 = self.date_cafter.date().toString('yyyy-MM-dd')
        print(date_str1, date_str2)
        sql = "SELECT * FROM covering WHERE 날짜 >= '" + date_str1 + "' and 날짜 <= '" + date_str2 + "'"

        print(sql)

        con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        row = 0
        col = 0
        self.table_csearch.setRowCount(len(rows))
        for i in rows:
            for j in i:
                print(j, end='  ')
                self.table_csearch.setItem(col, row, QTableWidgetItem(str(j)))
                row += 1
            row = 0
            col += 1
            print()

        con.close()

    def ksearch(self):
        self.label_kimpo.setVisible(False)
        self.table_ksearch.setRowCount(0)
        date_str1 = self.date_kbefore.date().toString('yyyy-MM-dd')
        date_str2 = self.date_kafter.date().toString('yyyy-MM-dd')
        print(date_str1, date_str2)
        sql = "SELECT * FROM covering WHERE 날짜 >= '" + date_str1 + "' and 날짜 <= '" + date_str2 + "'"

        print(sql)

        con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        row = 0
        col = 0
        self.table_ksearch.setRowCount(len(rows))
        for i in rows:
            for j in i:
                print(j, end='  ')
                self.table_ksearch.setItem(col, row, QTableWidgetItem(str(j)))
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
