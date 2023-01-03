import pymysql
import csv
import pandas as pd
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg


con = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock', charset='utf8')
cur = con.cursor()
# sql = "SELECT * FROM covering"
sql = "SELECT * FROM covering WHERE 날짜<'2018-01-05'"
cur.execute(sql)
rows = cur.fetchall()
day = []
covering_rate = []
print(type(rows))
for x in rows:
    day.append(x[0])
    covering_rate.append(x[6])
    print(x)
print(day)
print(covering_rate)
print(type(day))

# print(len(rows))
# print(rows[0])
# print(rows[0][0])
# print(rows[0][1])
# print(rows[0][2])
# print(rows[0][3])
# print(rows[0][4])
# print(rows[0][5])
# print(rows[0][6])
# print(type(rows[0][5]))

con.close()






form_class = uic.loadUiType("mainwindow.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        # self.a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # self.b = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        self.a = [1, 2, 3]
        self.b = [1.5, 2.0, 2.3]

        print(day)
        print(covering_rate)
        self.plot(self.a, self.b)

    def plot(self, hour, temperature):
        self.Graph1.plot(hour, temperature)  ## Graph1, Graph2 는 Designer에서 만든 위젯 이름

        # w = pg.PlotWidget(title="Basic Plot")


    # def show_main(self):
    #     self.stackedWidget.setCurrentIndex(0)


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
