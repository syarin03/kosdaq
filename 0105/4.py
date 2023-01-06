import pymysql
import pandas as pd
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import matplotlib
import numpy as np
import matplotlib.pyplot as plt



form_class = uic.loadUiType("main.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show_graph_btn.clicked.connect(self.show_graph)
        self.show_graph_btn2.clicked.connect(self.show_graph2)
        self.show_graph_btn3.clicked.connect(self.show_graph3)

        self.terms1_radio.clicked.connect(self.terms_function)
        self.terms2_radio.clicked.connect(self.terms_function)
        self.terms3_radio.clicked.connect(self.terms_function)

        self.start_date.dateChanged.connect(self.show_inner_graph)
        self.end_date.dateChanged.connect(self.show_inner_graph)
        self.start_date2.dateChanged.connect(self.show_inner_graph2)
        self.end_date2.dateChanged.connect(self.show_inner_graph2)
        self.start_date3.dateChanged.connect(self.show_inner_graph3)
        self.end_date3.dateChanged.connect(self.show_inner_graph3)
        self.terms = 'A'
        self.graph1.setYRange(100, 1200)

        #####################################실행 화면 inner 그래프를 보여주기 위함 start
        start_date = self.start_date2.date().toString('yyyy-MM-dd')
        end_date = self.end_date2.date().toString('yyyy-MM-dd')

        con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock', charset='utf8')

        cur2 = con2.cursor()

        sql2 = f"SELECT * FROM kosdaq WHERE '{start_date}' <= 날짜 AND 날짜 <= '{end_date}'"

        cur2.execute(sql2)

        rows2 = cur2.fetchall()

        day = []
        trading_volume = []
        kosdaq_index = []

        for x in rows2:
            day.append(x[0])
            kosdaq_index.append(x[1])
            trading_volume.append((x[2]))

        con2.close()

        x_dict = dict(enumerate(day))
        print(x_dict)
        ticks = [list(zip(x_dict.keys(), x_dict.values()))]
        print(ticks)
        xax = self.graph1.getAxis('bottom')
        xax.setTicks(ticks)


        self.graph1.addLegend()
        self.graph1.setLabel('left', '코스닥')
        self.graph1.setLabel('bottom', '날짜')
        # self.graph1.setLabel('right', '반대매매')
        self.graph1.setLimits(yMin=0, yMax=1300)
        self.graph1.setLimits(xMin=0, xMax=1250)
        self.graph1.plot(list(range(len(day))), kosdaq_index, pen='red',
                         name='코스닥')  ## Graph1, Graph2 는 Designer에서 만든 위젯 이름


        #####################################실행 화면 inner 그래프를 보여주기 위함 end


    def show_inner_graph3(self):
        self.preview_label.setText("<코스닥, 금리 그래프 미리보기>")
        start_date = self.start_date3.date().toString('yyyy-MM-dd')
        end_date = self.end_date3.date().toString('yyyy-MM-dd')

        con1 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')
        con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')

        cur1 = con1.cursor()
        cur2 = con1.cursor()

        sql1 = f"SELECT * FROM baserate WHERE '{start_date}' <= 날짜 AND 날짜 <= '{end_date}'"  # sql = "SELECT * FROM covering"
        sql2 = f"SELECT * FROM kosdaq WHERE '{start_date}' <= 날짜 AND 날짜 <= '{end_date}'"

        cur1.execute(sql1)
        cur2.execute(sql2)

        rows1 = cur1.fetchall()
        rows2 = cur2.fetchall()

        day = []
        base_rate = []
        kosdaq_index = []

        for x in rows1:
            day.append(x[0])
            base_rate.append(x[1])
        for x in rows2:
            kosdaq_index.append(x[1])

        con1.close()
        con2.close()

        #####################################QT Designer 내부 그래프 start
        self.graph1.clear()
        x_dict = dict(enumerate(day))
        print(x_dict)
        ticks = [list(zip(x_dict.keys(), x_dict.values()))]
        print(ticks)
        xax = self.graph1.getAxis('bottom')
        xax.setTicks(ticks)

        # 반대 매매 차트에서 보이기 위해 *300
        for i in range(len(base_rate)):
            base_rate[i] *= 300
        print(base_rate)

        self.graph1.addLegend()
        self.graph1.setLabel('left', '코스닥')
        self.graph1.setLabel('bottom', '날짜')
        # self.graph1.setLabel('right', '반대매매')
        self.graph1.setLimits(yMin=0, yMax=1300)
        self.graph1.setLimits(xMin=0, xMax=1250)
        self.graph1.plot(list(range(len(day))), kosdaq_index, pen='red',
                         name='코스닥')  ## Graph1, Graph2 는 Designer에서 만든 위젯 이름
        self.graph1.plot(list(range(len(day))), base_rate, pen='green',
                         name='반대매매')  ## Graph1, Graph2 는 Designer에서 만든 위젯 이름
        #####################################QT Designer 내부 그래프 end


    def show_inner_graph2(self):
        self.preview_label.setText("<코스닥, 거래량 그래프 미리보기>")
        start_date = self.start_date2.date().toString('yyyy-MM-dd')
        end_date = self.end_date2.date().toString('yyyy-MM-dd')

        con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')

        cur2 = con2.cursor()

        sql2 = f"SELECT * FROM kosdaq WHERE '{start_date}' <= 날짜 AND 날짜 <= '{end_date}'"

        cur2.execute(sql2)

        rows2 = cur2.fetchall()

        day = []
        trading_volume = []
        kosdaq_index = []

        for x in rows2:
            day.append(x[0])
            kosdaq_index.append(x[1])
            trading_volume.append((x[2]))

        con2.close()

        #####################################QT Designer 내부 그래프 start
        self.graph1.clear()
        x_dict = dict(enumerate(day))
        print(x_dict)
        ticks = [list(zip(x_dict.keys(), x_dict.values()))]
        print(ticks)
        xax = self.graph1.getAxis('bottom')
        xax.setTicks(ticks)

        # 반대 매매 차트에서 보이기 위해 *300
        for i in range(len(trading_volume)):
            trading_volume[i] /= 300

        self.graph1.addLegend()
        self.graph1.setLabel('left', '코스닥')
        self.graph1.setLabel('bottom', '날짜')
        # self.graph1.setLabel('right', '반대매매')
        self.graph1.setLimits(yMin=0, yMax=1300)
        self.graph1.setLimits(xMin=0, xMax=1250)
        self.graph1.plot(list(range(len(day))), kosdaq_index, pen='red',
                         name='코스닥')  ## Graph1, Graph2 는 Designer에서 만든 위젯 이름
        self.graph1.plot(list(range(len(day))), trading_volume, pen='green',
                         name='거래량')  ## Graph1, Graph2 는 Designer에서 만든 위젯 이름
        #####################################QT Designer 내부 그래프 end


    def show_inner_graph(self):
        self.preview_label.setText("<코스닥, 반대매매 그래프 미리보기>")
        start_date = self.start_date.date().toString('yyyy-MM-dd')
        end_date = self.end_date.date().toString('yyyy-MM-dd')
        # print(start_date)
        # print(end_date)

        con1 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')
        con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')

        cur1 = con1.cursor()
        cur2 = con1.cursor()

        sql1 = f"SELECT * FROM covering WHERE '{start_date}' <= 날짜 AND 날짜 <= '{end_date}'"  # sql = "SELECT * FROM covering"
        sql2 = f"SELECT * FROM kosdaq WHERE '{start_date}' <= 날짜 AND 날짜 <= '{end_date}'"

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
        #####################################QT Designer 내부 그래프 start
        self.graph1.clear()
        x_dict = dict(enumerate(day))
        print(x_dict)
        ticks = [list(zip(x_dict.keys(), x_dict.values()))]
        print(ticks)
        xax = self.graph1.getAxis('bottom')
        xax.setTicks(ticks)

        # 반대 매매 차트에서 보이기 위해 *50
        for i in range(len(covering_rate)):
            covering_rate[i] *= 50

        self.graph1.addLegend()
        self.graph1.setLabel('left', '코스닥')
        self.graph1.setLabel('bottom', '날짜')
        # self.graph1.setLabel('right', '반대매매')
        self.graph1.setLimits(yMin=0, yMax=1300)
        self.graph1.setLimits(xMin=0, xMax=1250)
        self.graph1.plot(list(range(len(day))), kosdaq_index, pen='red',
                         name='코스닥')  ## Graph1, Graph2 는 Designer에서 만든 위젯 이름
        self.graph1.plot(list(range(len(day))), covering_rate, pen='green',
                         name='반대매매')  ## Graph1, Graph2 는 Designer에서 만든 위젯 이름
        #####################################QT Designer 내부 그래프 end


    def terms_function(self):
        if self.terms1_radio.isChecked():
            self.terms = 'A'
            print("A")
        elif self.terms2_radio.isChecked():
            self.terms = 'B'
            print("B")
        else:
            self.terms = 'C'
            print("C")

    def show_graph3(self):
        start_date = self.start_date3.date().toString('yyyy-MM-dd')
        end_date = self.end_date3.date().toString('yyyy-MM-dd')

        con1 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',charset='utf8')
        con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',charset='utf8')

        cur1 = con1.cursor()
        cur2 = con1.cursor()

        sql1 = f"SELECT * FROM baserate WHERE '{start_date}' <= 날짜 AND 날짜 <= '{end_date}'"   # sql = "SELECT * FROM covering"
        sql2 = f"SELECT * FROM kosdaq WHERE '{start_date}' <= 날짜 AND 날짜 <= '{end_date}'"

        cur1.execute(sql1)
        cur2.execute(sql2)

        rows1 = cur1.fetchall()
        rows2 = cur2.fetchall()

        day = []
        base_rate = []
        kosdaq_index = []

        for x in rows1:
            day.append(x[0])
            base_rate.append(x[1])
        for x in rows2:
            kosdaq_index.append(x[1])

        con1.close()
        con2.close()


        ################################################################################ 외부창 그래프 start
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (13, 8)
        plt.rcParams['font.size'] = 8

        matplotlib.rcParams['font.family'] = 'Malgun Gothic'
        matplotlib.rcParams['font.size'] = 10  # 글자크기
        matplotlib.rcParams['axes.unicode_minus'] = False  # 마이너스기호(-)가 깨지는 현상 방지

        fig, ax1 = plt.subplots()


        # data개수의 따라 x축 라벨을 설정 하기 위함 xstart
        xticks_list = []
        n=0
        if len(rows1) < 300:
            for i in range(len(rows1)):
                xticks_list.append(n)
                n += 15
        elif len(rows1) < 800:
            for i in range(len(rows1)):
                xticks_list.append(n)
                n += 40
        elif len(rows1) < 1300:
            for i in range(len(rows1)):
                xticks_list.append(n)
                n += 75
        # data개수의 따라 x축 라벨을 설정 하기 위함 end

        plt.xticks(xticks_list, rotation=45)                # x축 라벨 설정 및 라벨 각도 조정
        plt.ylabel('코스닥 지수')                             # 코스닥 Y축 바깥쪽 라벨 이름
        plt.ylim([0, 1200])                                 # 코스닥 Y축 범위 지정
        ax1.plot(day, kosdaq_index, color='red', label='코스닥')   # x축 day, y축 코스닥 지수 그래프 설정
        plt.legend(loc='upper left')                        # 코스닥 범례 좌상

        # max, min를 찾아서 표시해주기 위함 start
        dic = {y: x for x, y in zip(day, kosdaq_index)}
        ax1.patch.set_visible(False)
        plt.text(dic[max(dic)], max(dic), 'Max ' + str(max(dic)), color='r', fontweight='bold',
                 horizontalalignment='center', verticalalignment='bottom')
        plt.text(dic[min(dic)], min(dic), 'Min ' + str(min(dic)), color='r', fontweight='bold',
                 horizontalalignment='center', verticalalignment='top', zorder=1)
        # max, min를 찾아서 표시해주기 위함 end

        ax2 = ax1.twinx()                                   # 기존 x,y축에 또 추가 하기 위함.twinx()
        ax2.plot(day, base_rate, color='gray', label='기준금리')    #2번 째 그래프는 bar 형태

        plt.ylabel('기준금리')                            # 반대매매비율 Y축 바깥쪽 라벨
        plt.ylim([0, 5])                                   # 반대매매비율 Y축 범위 지정

        plt.legend(loc='upper right')  # 반대매매비율 범례 우상
        plt.show()
        ################################################################################ 외부창 그래프 end




    def show_graph2(self):
        start_date = self.start_date2.date().toString('yyyy-MM-dd')
        end_date = self.end_date2.date().toString('yyyy-MM-dd')

        con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',charset='utf8')

        cur2 = con2.cursor()

        sql2 = f"SELECT * FROM kosdaq WHERE '{start_date}' <= 날짜 AND 날짜 <= '{end_date}'"

        cur2.execute(sql2)

        rows2 = cur2.fetchall()

        day = []
        trading_volume = []
        kosdaq_index = []

        for x in rows2:
            day.append(x[0])
            kosdaq_index.append(x[1])
            trading_volume.append((x[2]))

        con2.close()


        ################################################################################ 그래프 시작
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (13, 8)
        plt.rcParams['font.size'] = 8

        matplotlib.rcParams['font.family'] = 'Malgun Gothic'
        matplotlib.rcParams['font.size'] = 10  # 글자크기
        matplotlib.rcParams['axes.unicode_minus'] = False  # 마이너스기호(-)가 깨지는 현상 방지

        fig, ax1 = plt.subplots()


        # data개수의 따라 x축 라벨을 설정 하기 위함 xstart
        xticks_list = []
        n=0
        # print(len(rows1))
        if len(rows2) < 300:
            for i in range(len(rows2)):
                xticks_list.append(n)
                n += 15
        elif len(rows2) < 800:
            for i in range(len(rows2)):
                xticks_list.append(n)
                n += 40
        elif len(rows2) < 1300:
            for i in range(len(rows2)):
                xticks_list.append(n)
                n += 75
        # data개수의 따라 x축 라벨을 설정 하기 위함 end

        plt.xticks(xticks_list, rotation=45)  # x축 라벨 설정 및 라벨 각도 조정
        plt.ylabel('코스닥 지수')  # 코스닥 Y축 바깥쪽 라벨 이름
        plt.ylim([0, 1200])  # 코스닥 Y축 범위 지정
        ax1.plot(day, kosdaq_index, color='red', label='코스닥')  # x축 day, y축 코스닥 지수 그래프 설정
        plt.legend(loc='upper left')  # 코스닥 범례 좌상

        # max, min를 찾아서 표시해주기 위함 start
        dic = {y: x for x, y in zip(day, kosdaq_index)}
        ax1.patch.set_visible(False)
        plt.text(dic[max(dic)], max(dic), 'Max ' + str(max(dic)), color='r', fontweight='bold',
                 horizontalalignment='center', verticalalignment='bottom')
        plt.text(dic[min(dic)], min(dic), 'Min ' + str(min(dic)), color='r', fontweight='bold',
                 horizontalalignment='center', verticalalignment='top', zorder=1)
        # max, min를 찾아서 표시해주기 위함 end

        ax2 = ax1.twinx()  # 기존 x,y축에 또 추가 하기 위함.twinx()
        ax2.bar(day, trading_volume, color='gray', label='거래량', width=0.5)  # 2번 째 그래프는 bar 형태

        plt.ylabel('반대매매비율')  # 반대매매비율 Y축 바깥쪽 라벨
        plt.ylim([45000, 500000])  # 반대매매비율 Y축 범위 지정
        # plt.annotate('반대 매매 최대', xy=(max1, covering_rate[max1]), xytext=(max1 + 1, covering_rate[max1] + 5),
        #              horizontalalignment='bottom', arrowprops={'color': 'green'})  # 매수포인트 화살표 표시


        plt.legend(loc='upper right')  # 반대매매비율 범례 우상
        plt.show()



    def show_graph(self):
        start_date = self.start_date.date().toString('yyyy-MM-dd')
        end_date = self.end_date.date().toString('yyyy-MM-dd')
        # print(start_date)
        # print(end_date)

        con1 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',charset='utf8')
        con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',charset='utf8')

        cur1 = con1.cursor()
        cur2 = con1.cursor()

        sql1 = f"SELECT * FROM covering WHERE '{start_date}' <= 날짜 AND 날짜 <= '{end_date}'"   # sql = "SELECT * FROM covering"
        sql2 = f"SELECT * FROM kosdaq WHERE '{start_date}' <= 날짜 AND 날짜 <= '{end_date}'"

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

        max1 = np.argmax(covering_rate)  # 최대 값의 위치 인덱스를 반환 함.

        move_average = []
        move_average_temp = []

        for x in covering_rate:                                  # 이동 평균 코드(3개 씩 평균)
            move_average_temp.append(x)
            if len(move_average_temp) == 3:
                suma = sum(move_average_temp) / 3
                move_average.append(round(suma, 3))
                move_average_temp.pop(0)
                covering_rate_count = 0

        abc = []

        for i in range(len(move_average) - 1):
            if move_average[i + 1] > move_average[i] * 1.4:
                abc.append(move_average[i + 1])

        ################################################################################ 그래프 시작
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (13, 8)
        plt.rcParams['font.size'] = 8

        matplotlib.rcParams['font.family'] = 'Malgun Gothic'
        matplotlib.rcParams['font.size'] = 10  # 글자크기
        matplotlib.rcParams['axes.unicode_minus'] = False  # 마이너스기호(-)가 깨지는 현상 방지

        fig, ax1 = plt.subplots()


        # data개수의 따라 x축 라벨을 설정 하기 위함 xstart
        xticks_list = []
        n=0
        if len(rows1) < 300:
            for i in range(len(rows1)):
                xticks_list.append(n)
                n += 15
        elif len(rows1) < 800:
            for i in range(len(rows1)):
                xticks_list.append(n)
                n += 40
        elif len(rows1) < 1300:
            for i in range(len(rows1)):
                xticks_list.append(n)
                n += 75
        # data개수의 따라 x축 라벨을 설정 하기 위함 end

        plt.xticks(xticks_list, rotation=45)                # x축 라벨 설정 및 라벨 각도 조정
        plt.ylabel('코스닥 지수')                             # 코스닥 Y축 바깥쪽 라벨 이름
        plt.ylim([0, 1200])                                 # 코스닥 Y축 범위 지정
        ax1.plot(day, kosdaq_index, color='red', label='코스닥')   # x축 day, y축 코스닥 지수 그래프 설정
        plt.legend(loc='upper left')                        # 코스닥 범례 좌상


        # max, min를 찾아서 표시해주기 위함 start
        dic = {y: x for x, y in zip(day, kosdaq_index)}
        ax1.patch.set_visible(False)
        plt.text(dic[max(dic)], max(dic), 'Max ' + str(max(dic)), color='r', fontweight='bold',
                 horizontalalignment='center', verticalalignment='bottom')
        plt.text(dic[min(dic)], min(dic), 'Min ' + str(min(dic)), color='r', fontweight='bold',
                 horizontalalignment='center', verticalalignment='top', zorder=1)
        # max, min를 찾아서 표시해주기 위함 end

        ax2 = ax1.twinx()                                   # 기존 x,y축에 또 추가 하기 위함.twinx()
        ax2.bar(day, covering_rate, color='gray', label='반대매매비율', width=0.5)    #2번 째 그래프는 bar 형태

        plt.ylabel('반대매매비율')                            # 반대매매비율 Y축 바깥쪽 라벨
        plt.ylim([0, 25])                                   # 반대매매비율 Y축 범위 지정
        # plt.annotate('반대 매매 최대', xy=(max1, covering_rate[max1]), xytext=(max1 + 1, covering_rate[max1] + 5),
        #              horizontalalignment='bottom', arrowprops={'color': 'green'})  # 매수포인트 화살표 표시

        # 매수 지점 조건 화살표 표시 start(1. 반대매매 지수 값 조건)
        if self.terms == 'A':
            power_count = 0
            for x in covering_rate:
                power_count += 1
                if x > float(self.terms1_edit.text()):
                    plt.annotate('강력 매수!', xy=(power_count - 1, x), xytext=(power_count - 1, x + 3), horizontalalignment='center', arrowprops={'color': 'red'})  # 매수포인트 화살표 표시
        # 매수 지점 조건 화살표 표시 end

        # 매수 지점 조건 화살표 표시 start(2. 반대매매 지수 평균 값 조건)
        if self.terms == 'B':
            power_count = 0
            covering_rate_avg = sum(covering_rate) / len(covering_rate)
            print(covering_rate_avg)
            for x in covering_rate:
                power_count += 1
                if x > covering_rate_avg*float(self.terms2_edit.text()):
                    plt.annotate('강력 매수!', xy=(power_count - 1, x), xytext=(power_count - 1, x + 3), horizontalalignment='center', arrowprops={'color': 'red'})  # 매수포인트 화살표 표시
        # 매수 지점 조건 화살표 표시 end

        # 매수 지점 조건 화살표 표시 start(3. 반대매매 2가지 조건)
        if self.terms == 'C':
            power_count = 0
            covering_rate_avg = sum(covering_rate) / len(covering_rate)
            print(covering_rate_avg)
            for x in covering_rate:
                power_count += 1
                if x > covering_rate_avg * float(self.terms2_edit.text()) and x > float(self.terms1_edit.text()):
                    plt.annotate('강력 매수!', xy=(power_count - 1, x), xytext=(power_count - 1, x + 3),
                                 horizontalalignment='center', arrowprops={'color': 'red'})  # 매수포인트 화살표 표시
        # 매수 지점 조건 화살표 표시 end

        plt.legend(loc='upper right')  # 반대매매비율 범례 우상
        plt.show()





if __name__ == "__main__" :
    app = QApplication(sys.argv)            #QApplication : 프로그램을 실행시켜주는 클래스
    myWindow = WindowClass()                #WindowClass의 인스턴스 생성
    myWindow.show()                         #프로그램 화면을 보여주는 코드
    app.exec_()                             #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드