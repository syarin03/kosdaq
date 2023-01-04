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
import datetime

form_class = uic.loadUiType("main.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show_graph_btn.clicked.connect(self.show_graph)


    # def show_graph(self):
    #     print("a")
    #     start_date = self.start_date.date()
    #     end_date = self.end_date.date()
    #     start_year = start_date.year()
    #     start_month = start_date.month()
    #     start_day = start_date.day()
    #     end_year = end_date.year()
    #     end_month = end_date.month()
    #     end_day = end_date.day()
    #     print(start_date)
    #     print(end_date)
    #     print(start_year)
    #     print(start_month)
    #     print(start_day)
    #     print(end_year)
    #     print(end_month)
    #     print(end_day)


    def show_graph(self):
        start_date = self.start_date.date().toString('yyyy-MM-dd')
        end_date = self.end_date.date().toString('yyyy-MM-dd')
        print(start_date)
        print(end_date)


        con1 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',charset='utf8')
        con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',charset='utf8')

        cur1 = con1.cursor()
        cur2 = con1.cursor()
        # print(type(end_year))
        # date_str1 = str(end_year)+'-'+str(end_month)+'-'+str(end_day)
        # print('9')
        # print(date_str1)
        # print(type(date_str1))
        # date_str2 = "2022-01-03"


        # abcd = "SELECT * FROM covering WHERE 날짜<'"+str(end_year)+'-'+str(end_month)+'-'+str(end_day)+"'"
        # print(abcd)
        sql1 = f"SELECT * FROM covering WHERE 날짜 <'{end_date}'"   # sql = "SELECT * FROM covering"
        sql2 = f"SELECT * FROM kosdaq WHERE 날짜 <'{end_date}'"
        # sql2 = abcd

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

        con1.close()
        con2.close()

        # print(day)
        print(covering_rate)
        print(kosdaq_index)

        max1 = np.argmax(covering_rate)  # 최대 값의 위치 인덱스를 반환 함.
        print(max1)
        print(covering_rate[max1])

        print(len(covering_rate))

        move_average = []
        move_average_temp = []

        for x in covering_rate:  # 이동 평균 코드(3개 씩 평균)
            move_average_temp.append(x)
            if len(move_average_temp) == 3:
                suma = sum(move_average_temp) / 3
                move_average.append(round(suma, 3))
                move_average_temp.pop(0)
                covering_rate_count = 0

        print(move_average)
        abc = []

        for i in range(len(move_average) - 1):
            if move_average[i + 1] > move_average[i] * 1.4:
                abc.append(move_average[i + 1])
        print(abc)

        for i in range(len(abc)):
            print(move_average.index(abc[i]) * 3)

        ################################################################################ 그래프 시작
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (13, 8)
        plt.rcParams['font.size'] = 8

        matplotlib.rcParams['font.family'] = 'Malgun Gothic'
        matplotlib.rcParams['font.size'] = 10  # 글자크기
        matplotlib.rcParams['axes.unicode_minus'] = False  # 마이너스기호(-)가 깨지는 현상 방지

        fig, ax1 = plt.subplots()

        # plt.xticks(
        #     [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300, 315, 330,
        #      345, 360, 375, 390, 405, 420, 435, 450, 465, 480, 495, 510, 525, 540, 555, 570, 585, 600], rotation=45)
        plt.xticks(rotation=45)
        plt.ylabel('코스닥 지수')  # 코스닥 Y축 바깥쪽 라벨
        plt.ylim([0, 1200])  # 코스닥 Y축 범위 지정
        ax1.plot(day, kosdaq_index, color='red', label='코스닥')
        plt.legend(loc='upper left')  # 코스닥 범례 좌상

        dic = {y: x for x, y in zip(day, kosdaq_index)}
        ax1.patch.set_visible(False)
        plt.text(dic[max(dic)], max(dic), 'Max ' + str(max(dic)), color='r', fontweight='bold',
                 horizontalalignment='center', verticalalignment='bottom')
        plt.text(dic[min(dic)], min(dic), 'Min ' + str(min(dic)), color='r', fontweight='bold',
                 horizontalalignment='center', verticalalignment='top', zorder=1)

        ax2 = ax1.twinx()
        ax2.bar(day, covering_rate, color='gray', label='반대매매비율', width=0.5)

        plt.ylabel('반대매매비율')  # 반대매매비율 Y축 바깥쪽 라벨
        plt.ylim([0, 25])  # 반대매매비율 Y축 범위 지정
        # plt.annotate('반대 매매 최대', xy=(max1, covering_rate[max1]), xytext=(max1 + 1, covering_rate[max1] + 5),
        #              horizontalalignment='bottom', arrowprops={'color': 'green'})  # 매수포인트 화살표 표시

        power_count = 0
        for x in covering_rate:
            power_count += 1
            if x > 9:
                plt.annotate('강력 매수!', xy=(power_count - 1, x), xytext=(power_count - 1, x + 3),
                             horizontalalignment='center', arrowprops={'color': 'red'})  # 매수포인트 화살표 표시

        plt.legend(loc='upper right')  # 반대매매비율 범례 우상
        plt.show()






if __name__ == "__main__" :
    app = QApplication(sys.argv)            #QApplication : 프로그램을 실행시켜주는 클래스
    myWindow = WindowClass()                #WindowClass의 인스턴스 생성
    myWindow.show()                         #프로그램 화면을 보여주는 코드
    app.exec_()                             #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드