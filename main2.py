import pymysql
import csv
import pandas as pd
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np






con1 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock', charset='utf8')
con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock', charset='utf8')

cur1 = con1.cursor()
cur2 = con1.cursor()

sql1 = "SELECT * FROM covering WHERE 날짜<'2019-01-30'"           # sql = "SELECT * FROM covering"
sql2 = "SELECT * FROM kosdaq WHERE 날짜<'2019-01-30'"

cur1.execute(sql1)
cur2.execute(sql2)

rows1 = cur1.fetchall()
rows2 = cur2.fetchall()

day = []
covering_rate = []
kosdaq_index = []

for x in rows1:
    day.append(x[0])
    covering_rate.append(x[6])
for x in rows2:
    kosdaq_index.append(x[1])


print(day)
print(covering_rate)
print(kosdaq_index)

con1.close()
con2.close()

max1 = np.argmax(covering_rate)
print(max1)
print(rows1)



plt.style.use('default')
plt.rcParams['figure.figsize'] = (13, 8)
plt.rcParams['font.size'] = 8

matplotlib.rcParams['font.family'] ='Malgun Gothic'
matplotlib.rcParams['font.size'] = 10 # 글자크기
matplotlib.rcParams['axes.unicode_minus'] = False                                   # 마이너스기호(-)가 깨지는 현상 방지


fig, ax1 = plt.subplots()
plt.xticks([0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345, 360, 375, 390, 405, 420, 435, 450, 465, 480, 495, 510, 525, 540, 555, 570, 585, 600], rotation=45)
plt.ylabel('코스닥 지수')                                                            # 코스닥 Y축 바깥쪽 라벨
plt.ylim([200, 1000])                                                               # 코스닥 Y축 범위 지정
ax1.plot(day, kosdaq_index, color='red', label='코스닥')
plt.legend(loc='upper left')                                                        # 코스닥 범례 좌상

ax2 = ax1.twinx()
ax2.bar(day, covering_rate, color='gray', label='반대매매비율', width=0.4)
plt.ylabel('반대매매비율')                                                            # 반대매매비율 Y축 바깥쪽 라벨
plt.ylim([0, 20])                                                                   # 반대매매비율 Y축 범위 지정

# ax2.set_xticks([0, 30, 60, 90])
# ax3 = ax2.twinx()
# ax3.plot(day, covering_rate, color='blue', marker='o', linestyle='')


plt.legend(loc='upper right')                                                       # 반대매매비율 범례 우상
plt.show()


# plt.figure(figsize=(10,5))
#
# plt.plot(day, kosdaq_index, color='blue', label='코스닥')
# plt.plot(day, covering_rate, color='red', label='반대매매')
#
# plt.title("코스닥 지수")
# plt.xticks(rotation=45)
# plt.xlabel("날짜")
# plt.ylabel("지수")
#
# plt.legend()
#
#
# plt.show()








#
#
#
#
# form_class = uic.loadUiType("mainwindow.ui")[0]
#
# class WindowClass(QMainWindow, form_class) :
#     def __init__(self) :
#         super().__init__()
#         self.setupUi(self)
        # self.a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # self.b = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        # self.a = [1, 2, 3]
        # self.b = [1.5, 2.0, 2.3]
        # # print(day)
        # # print(covering_rate)
        # # self.plot(self.a, self.b)
        # plt.title('abc')
        # plt.plot(self.a, self.b, color='red', label = 'up')
        # plt.legend()
        #
        # plt.show()

#     # def plot(self, hour, temperature):
#     #     self.Graph1.plot(hour, temperature)  ## Graph1, Graph2 는 Designer에서 만든 위젯 이름
#
#         # w = pg.PlotWidget(title="Basic Plot")
#
#
#     # def show_main(self):
#     #     self.stackedWidget.setCurrentIndex(0)
#
#
# if __name__ == "__main__" :
#     #QApplication : 프로그램을 실행시켜주는 클래스
#     app = QApplication(sys.argv)
#     #WindowClass의 인스턴스 생성
#     myWindow = WindowClass()
#     #프로그램 화면을 보여주는 코드
#     myWindow.show()
#     #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
#     app.exec_()
