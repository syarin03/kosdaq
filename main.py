import pymysql
import pandas as pd
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

form_class = uic.loadUiType("main.ui")[0]

host_str = '10.10.21.116'
user_str = 'stock_admin'
password_str = 'admin1234'


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        today = QDate.currentDate()

        self.terms = 'A'
        self.graph1.setYRange(100, 1200)

        # 스택 기본 페이지 설정
        self.stackedWidget.setCurrentWidget(self.stack_main)
        self.tab_search.setCurrentWidget(self.kosdaq_tab_search)
        self.tab_manage.setCurrentWidget(self.kosdaq_tab)
        self.kosdaq_tab_manage.setCurrentWidget(self.kosdaq_tab_add)
        self.covering_tab_manage.setCurrentWidget(self.covering_tab_add)
        self.baserate_tab_manage.setCurrentWidget(self.baserate_tab_add)

        # 조회 날짜 선택 경고 라벨 Invisible
        self.kosdaq_label_impossible.setVisible(False)
        self.covering_label_impossible.setVisible(False)
        self.baserate_label_impossible.setVisible(False)

        # 날짜 기본값 설정
        self.kosdaq_date_add.setDate(today)
        self.kosdaq_date_del.setDate(today)
        self.kosdaq_date_edit.setDate(today)
        self.covering_date_add.setDate(today)
        self.covering_date_del.setDate(today)
        self.covering_date_edit.setDate(today)
        self.baserate_date_add.setDate(today)
        self.baserate_date_del.setDate(today)
        self.baserate_date_edit.setDate(today)
        self.kosdaq_date_add.setMaximumDate(today)
        self.kosdaq_date_del.setMaximumDate(today)
        self.kosdaq_date_edit.setMaximumDate(today)
        self.covering_date_add.setMaximumDate(today)
        self.covering_date_del.setMaximumDate(today)
        self.covering_date_edit.setMaximumDate(today)
        self.baserate_date_add.setMaximumDate(today)
        self.baserate_date_del.setMaximumDate(today)
        self.baserate_date_edit.setMaximumDate(today)
        self.set_date_minimum()
        self.kosdaq_date_after.setDate(today)
        self.kosdaq_date_before.setMaximumDate(today)
        self.kosdaq_date_after.setMaximumDate(today)
        self.covering_date_after.setDate(today)
        self.covering_date_before.setMaximumDate(today)
        self.covering_date_after.setMaximumDate(today)
        self.baserate_date_after.setDate(today)
        self.baserate_date_before.setMaximumDate(today)
        self.baserate_date_after.setMaximumDate(today)

        # clicked 이벤트
        self.btn_go_manage.clicked.connect(self.go_manage)
        self.btn_go_search.clicked.connect(self.go_search)
        self.btn_go_graph.clicked.connect(self.go_graph)
        self.btn_search_to_main.clicked.connect(self.go_main)
        self.btn_manage_to_main.clicked.connect(self.go_main)
        self.btn_graph_to_main.clicked.connect(self.go_main)
        self.kosdaq_btn_search.clicked.connect(self.table_search)
        self.covering_btn_search.clicked.connect(self.table_search)
        self.baserate_btn_search.clicked.connect(self.table_search)
        self.kosdaq_btn_addDate.clicked.connect(self.set_group)
        self.kosdaq_btn_delDate.clicked.connect(self.set_group)
        self.kosdaq_btn_editDate.clicked.connect(self.set_group)
        self.covering_btn_addDate.clicked.connect(self.set_group)
        self.covering_btn_delDate.clicked.connect(self.set_group)
        self.covering_btn_editDate.clicked.connect(self.set_group)
        self.baserate_btn_addDate.clicked.connect(self.set_group)
        self.baserate_btn_delDate.clicked.connect(self.set_group)
        self.baserate_btn_editDate.clicked.connect(self.set_group)
        self.kosdaq_btn_add.clicked.connect(self.add_data)
        self.kosdaq_btn_del.clicked.connect(self.del_data)
        self.kosdaq_btn_edit.clicked.connect(self.edit_data)
        self.covering_btn_add.clicked.connect(self.add_data)
        self.covering_btn_del.clicked.connect(self.del_data)
        self.covering_btn_edit.clicked.connect(self.edit_data)
        self.baserate_btn_add.clicked.connect(self.add_data)
        self.baserate_btn_del.clicked.connect(self.del_data)
        self.baserate_btn_edit.clicked.connect(self.edit_data)
        self.graph_btn_show1.clicked.connect(self.show_graph1)
        self.graph_btn_show2.clicked.connect(self.show_graph2)
        self.graph_btn_show3.clicked.connect(self.show_graph3)
        self.graph_radio_terms1.clicked.connect(self.terms_function)
        self.graph_radio_terms2.clicked.connect(self.terms_function)
        self.graph_radio_terms3.clicked.connect(self.terms_function)

        # dateChanged 이벤트
        self.kosdaq_date_before.dateChanged.connect(self.set_date)
        self.kosdaq_date_after.dateChanged.connect(self.set_date)
        self.covering_date_before.dateChanged.connect(self.set_date)
        self.covering_date_after.dateChanged.connect(self.set_date)
        self.baserate_date_before.dateChanged.connect(self.set_date)
        self.baserate_date_after.dateChanged.connect(self.set_date)
        self.kosdaq_date_add.dateChanged.connect(self.set_date_sel_button)
        self.kosdaq_date_del.dateChanged.connect(self.set_date_sel_button)
        self.kosdaq_date_edit.dateChanged.connect(self.set_date_sel_button)
        self.covering_date_add.dateChanged.connect(self.set_date_sel_button)
        self.covering_date_del.dateChanged.connect(self.set_date_sel_button)
        self.covering_date_edit.dateChanged.connect(self.set_date_sel_button)
        self.baserate_date_add.dateChanged.connect(self.set_date_sel_button)
        self.baserate_date_del.dateChanged.connect(self.set_date_sel_button)
        self.baserate_date_edit.dateChanged.connect(self.set_date_sel_button)
        self.graph_date_start1.dateChanged.connect(self.show_inner_graph1)
        self.graph_date_end1.dateChanged.connect(self.show_inner_graph1)
        self.graph_date_start2.dateChanged.connect(self.show_inner_graph2)
        self.graph_date_end2.dateChanged.connect(self.show_inner_graph2)
        self.graph_date_start3.dateChanged.connect(self.show_inner_graph3)
        self.graph_date_end3.dateChanged.connect(self.show_inner_graph3)

        # currentChanged 이벤트
        self.tab_search.currentChanged.connect(self.reset_tab)
        self.tab_manage.currentChanged.connect(self.reset_tab)
        self.kosdaq_tab_manage.currentChanged.connect(self.reset_tab)
        self.covering_tab_manage.currentChanged.connect(self.reset_tab)
        self.baserate_tab_manage.currentChanged.connect(self.reset_tab)

# --이현도: 매수/매도 시점 분석 자료 그래프 시각화
        graph_date_start = self.graph_date_start2.date().toString('yyyy-MM-dd')
        graph_date_end = self.graph_date_end2.date().toString('yyyy-MM-dd')

        day = []
        trading_volume = []
        kosdaq_index = []

        con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock',
                              charset='utf8')

        with con:
            with con.cursor() as cur:
                sql = f"SELECT * FROM kosdaq WHERE '{graph_date_start}' <= 날짜 AND 날짜 <= '{graph_date_end}'"
                cur.execute(sql)
                rows = cur.fetchall()
                for x in rows:
                    day.append(x[0])
                    kosdaq_index.append(x[1])
                    trading_volume.append((x[2]))

        x_dict = dict(enumerate(day))
        # print(x_dict)
        ticks = [list(zip(x_dict.keys(), x_dict.values()))]
        # print(ticks)
        xax = self.graph1.getAxis('bottom')
        xax.setTicks(ticks)

        self.graph1.addLegend()
        self.graph1.setLabel('left', '코스닥')
        self.graph1.setLabel('bottom', '날짜')
        # self.graph1.setLabel('right', '반대매매')
        self.graph1.setLimits(yMin=0, yMax=1300)
        self.graph1.setLimits(xMin=0, xMax=1250)
        self.graph1.plot(list(range(len(day))), kosdaq_index, pen='red', name='코스닥')

    def set_date_minimum(self):
        sql_kosdaq = f"SELECT * FROM kosdaq ORDER BY 날짜"
        sql_covering = f"SELECT * FROM covering ORDER BY 날짜"
        sql_baserate = f"SELECT * FROM baserate ORDER BY 날짜"

        con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
        with con:
            with con.cursor() as cur:
                cur.execute(sql_kosdaq)
                result_kosdaq = cur.fetchall()
                self.kosdaq_date_before.setMinimumDate(QDate.fromString(result_kosdaq[0][0], 'yyyy-MM-dd'))
                cur.execute(sql_covering)
                result_covering = cur.fetchall()
                self.covering_date_before.setMinimumDate(QDate.fromString(result_covering[0][0], 'yyyy-MM-dd'))
                cur.execute(sql_baserate)
                result_baserate = cur.fetchall()
                self.baserate_date_before.setMinimumDate(QDate.fromString(result_baserate[0][0], 'yyyy-MM-dd'))

    def terms_function(self):
        if self.graph_radio_terms1.isChecked():
            self.terms = 'A'
            print("A")
        elif self.graph_radio_terms2.isChecked():
            self.terms = 'B'
            print("B")
        else:
            self.terms = 'C'
            print("C")

    def show_graph1(self):
        graph_date_start = self.graph_date_start1.date().toString('yyyy-MM-dd')
        graph_date_end = self.graph_date_end1.date().toString('yyyy-MM-dd')
        # print(graph_date_start)
        # print(graph_date_end)

        con1 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')
        con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')

        cur1 = con1.cursor()
        cur2 = con1.cursor()

        sql1 = f"SELECT * FROM covering WHERE '{graph_date_start}' <= 날짜 AND 날짜 <= '{graph_date_end}'"  # sql = "SELECT * FROM covering"
        sql2 = f"SELECT * FROM kosdaq WHERE '{graph_date_start}' <= 날짜 AND 날짜 <= '{graph_date_end}'"

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

        for x in covering_rate:  # 이동 평균 코드(3개 씩 평균)
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
        n = 0
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
        ax2.bar(day, covering_rate, color='gray', label='반대매매비율', width=0.5)  # 2번 째 그래프는 bar 형태

        plt.ylabel('반대매매비율')  # 반대매매비율 Y축 바깥쪽 라벨
        plt.ylim([0, 25])  # 반대매매비율 Y축 범위 지정
        # plt.annotate('반대 매매 최대', xy=(max1, covering_rate[max1]), xytext=(max1 + 1, covering_rate[max1] + 5),
        #              horizontalalignment='bottom', arrowprops={'color': 'green'})  # 매수포인트 화살표 표시

        # 매수 지점 조건 화살표 표시 start(1. 반대매매 지수 값 조건)
        if self.terms == 'A':
            power_count = 0
            for x in covering_rate:
                power_count += 1
                if x > float(self.graph_edit_terms1.text()):
                    plt.annotate('강력 매수!', xy=(power_count - 1, x), xytext=(power_count - 1, x + 3),
                                 horizontalalignment='center', arrowprops={'color': 'red'})  # 매수포인트 화살표 표시
        # 매수 지점 조건 화살표 표시 end

        # 매수 지점 조건 화살표 표시 start(2. 반대매매 지수 평균 값 조건)
        if self.terms == 'B':
            power_count = 0
            covering_rate_avg = sum(covering_rate) / len(covering_rate)
            print(covering_rate_avg)
            for x in covering_rate:
                power_count += 1
                if x > covering_rate_avg * float(self.graph_edit_terms2.text()):
                    plt.annotate('강력 매수!', xy=(power_count - 1, x), xytext=(power_count - 1, x + 3),
                                 horizontalalignment='center', arrowprops={'color': 'red'})  # 매수포인트 화살표 표시
        # 매수 지점 조건 화살표 표시 end

        # 매수 지점 조건 화살표 표시 start(3. 반대매매 2가지 조건)
        if self.terms == 'C':
            power_count = 0
            covering_rate_avg = sum(covering_rate) / len(covering_rate)
            print(covering_rate_avg)
            for x in covering_rate:
                power_count += 1
                if x > covering_rate_avg * float(self.graph_edit_terms2.text()) and x > float(
                        self.graph_edit_terms1.text()):
                    plt.annotate('강력 매수!', xy=(power_count - 1, x), xytext=(power_count - 1, x + 3),
                                 horizontalalignment='center', arrowprops={'color': 'red'})  # 매수포인트 화살표 표시
        # 매수 지점 조건 화살표 표시 end

        plt.legend(loc='upper right')  # 반대매매비율 범례 우상
        plt.show()

    def show_graph2(self):
        graph_date_start = self.graph_date_start2.date().toString('yyyy-MM-dd')
        graph_date_end = self.graph_date_end2.date().toString('yyyy-MM-dd')

        con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')

        cur2 = con2.cursor()

        sql2 = f"SELECT * FROM kosdaq WHERE '{graph_date_start}' <= 날짜 AND 날짜 <= '{graph_date_end}'"

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
        n = 0
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

    def show_graph3(self):
        graph_date_start = self.graph_date_start3.date().toString('yyyy-MM-dd')
        graph_date_end = self.graph_date_end3.date().toString('yyyy-MM-dd')

        con1 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')
        con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')

        cur1 = con1.cursor()
        cur2 = con1.cursor()

        sql1 = f"SELECT * FROM baserate WHERE '{graph_date_start}' <= 날짜 AND 날짜 <= '{graph_date_end}'"  # sql = "SELECT * FROM covering"
        sql2 = f"SELECT * FROM kosdaq WHERE '{graph_date_start}' <= 날짜 AND 날짜 <= '{graph_date_end}'"

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
        n = 0
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
        ax2.plot(day, base_rate, color='gray', label='기준금리')  # 2번 째 그래프는 bar 형태

        plt.ylabel('기준금리')  # 반대매매비율 Y축 바깥쪽 라벨
        plt.ylim([0, 5])  # 반대매매비율 Y축 범위 지정

        plt.legend(loc='upper right')  # 반대매매비율 범례 우상
        plt.show()
        ################################################################################ 외부창 그래프 end

    def show_inner_graph3(self):
        self.graph_label_preview.setText("<코스닥, 금리 그래프 미리보기>")
        graph_date_start = self.graph_date_start3.date().toString('yyyy-MM-dd')
        graph_date_end = self.graph_date_end3.date().toString('yyyy-MM-dd')

        con1 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')
        con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')

        cur1 = con1.cursor()
        cur2 = con1.cursor()

        sql1 = f"SELECT * FROM baserate WHERE '{graph_date_start}' <= 날짜 AND 날짜 <= '{graph_date_end}'"  # sql = "SELECT * FROM covering"
        sql2 = f"SELECT * FROM kosdaq WHERE '{graph_date_start}' <= 날짜 AND 날짜 <= '{graph_date_end}'"

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
        self.graph_label_preview.setText("<코스닥, 거래량 그래프 미리보기>")
        graph_date_start = self.graph_date_start2.date().toString('yyyy-MM-dd')
        graph_date_end = self.graph_date_end2.date().toString('yyyy-MM-dd')

        con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')

        cur2 = con2.cursor()

        sql2 = f"SELECT * FROM kosdaq WHERE '{graph_date_start}' <= 날짜 AND 날짜 <= '{graph_date_end}'"

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

    def show_inner_graph1(self):
        self.graph_label_preview.setText("<코스닥, 반대매매 그래프 미리보기>")
        graph_date_start = self.graph_date_start1.date().toString('yyyy-MM-dd')
        graph_date_end = self.graph_date_end1.date().toString('yyyy-MM-dd')
        # print(graph_date_start)
        # print(graph_date_end)

        con1 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')
        con2 = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock',
                               charset='utf8')

        cur1 = con1.cursor()
        cur2 = con1.cursor()

        sql1 = f"SELECT * FROM covering WHERE '{graph_date_start}' <= 날짜 AND 날짜 <= '{graph_date_end}'"  # sql = "SELECT * FROM covering"
        sql2 = f"SELECT * FROM kosdaq WHERE '{graph_date_start}' <= 날짜 AND 날짜 <= '{graph_date_end}'"

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

# --류가미: 데이터 조회/추가/삭제/수정
    def go_main(self):
        """메인 페이지 스택으로 이동"""
        self.stackedWidget.setCurrentWidget(self.stack_main)

    def go_manage(self):
        """데이터 관리 스택으로 이동"""
        self.stackedWidget.setCurrentWidget(self.stack_manage)

    def go_search(self):
        """데이터 조회 스택으로 이동"""
        self.stackedWidget.setCurrentWidget(self.stack_search)

    def go_graph(self):
        """그래프 스택으로 이동"""
        self.stackedWidget.setCurrentWidget(self.stack_graph)

    def reset_tab(self):
        """탭 또는 스택 이동 시 tableWidget과 label을 전부 초기화 함"""
        self.kosdaq_table.setRowCount(0)
        self.covering_table.setRowCount(0)
        self.baserate_table.setRowCount(0)

        self.kosdaq_group_add.setEnabled(False)
        self.kosdaq_group_del.setEnabled(False)
        self.kosdaq_group_edit.setEnabled(False)

        self.kosdaq_spin_add1.setValue(0)
        self.kosdaq_spin_add2.setValue(0)
        self.kosdaq_spin_add3.setValue(0)
        self.kosdaq_spin_add4.setValue(0)
        self.kosdaq_spin_add5.setValue(0)
        self.kosdaq_spin_add6.setValue(0)

        self.kosdaq_label_del1.clear()
        self.kosdaq_label_del2.clear()
        self.kosdaq_label_del3.clear()
        self.kosdaq_label_del4.clear()
        self.kosdaq_label_del5.clear()
        self.kosdaq_label_del6.clear()

        self.kosdaq_label_edit1.clear()
        self.kosdaq_label_edit2.clear()
        self.kosdaq_label_edit3.clear()
        self.kosdaq_label_edit4.clear()
        self.kosdaq_label_edit5.clear()
        self.kosdaq_label_edit6.clear()

        self.kosdaq_spin_edit1.setValue(0)
        self.kosdaq_spin_edit2.setValue(0)
        self.kosdaq_spin_edit3.setValue(0)
        self.kosdaq_spin_edit4.setValue(0)
        self.kosdaq_spin_edit5.setValue(0)
        self.kosdaq_spin_edit6.setValue(0)

        self.covering_spin_add1.setValue(0)
        self.covering_spin_add2.setValue(0)
        self.covering_spin_add3.setValue(0)
        self.covering_spin_add4.setValue(0)
        self.covering_spin_add5.setValue(0)
        self.covering_spin_add6.setValue(0)

        self.covering_label_del1.clear()
        self.covering_label_del2.clear()
        self.covering_label_del3.clear()
        self.covering_label_del4.clear()
        self.covering_label_del5.clear()
        self.covering_label_del6.clear()

        self.covering_label_edit1.clear()
        self.covering_label_edit2.clear()
        self.covering_label_edit3.clear()
        self.covering_label_edit4.clear()
        self.covering_label_edit5.clear()
        self.covering_label_edit6.clear()

        self.covering_spin_edit1.setValue(0)
        self.covering_spin_edit2.setValue(0)
        self.covering_spin_edit3.setValue(0)
        self.covering_spin_edit4.setValue(0)
        self.covering_spin_edit5.setValue(0)
        self.covering_spin_edit6.setValue(0)

        self.baserate_spin_add1.setValue(0)

        self.baserate_label_del1.clear()

        self.baserate_label_edit1.clear()

        self.baserate_spin_edit1.setValue(0)

    def set_date(self):
        """끝 날짜 선택 시 시작 날짜보다 이전 날짜를 선택하지 못하게 하기 위해 시작 날짜와 동일하게 바꿈"""
        if self.kosdaq_date_before.date() > self.kosdaq_date_after.date():
            self.kosdaq_date_after.setDate(self.kosdaq_date_before.date())
            self.kosdaq_label_impossible.setVisible(True)
        else:
            self.kosdaq_label_impossible.setVisible(False)

        if self.covering_date_before.date() > self.covering_date_after.date():
            self.covering_date_after.setDate(self.covering_date_before.date())
            self.covering_label_impossible.setVisible(True)
        else:
            self.covering_label_impossible.setVisible(False)

        if self.baserate_date_before.date() > self.baserate_date_after.date():
            self.baserate_date_after.setDate(self.baserate_date_before.date())
            self.baserate_label_impossible.setVisible(True)
        else:
            self.baserate_label_impossible.setVisible(False)

    def set_date_sel_button(self):
        """해당 날짜에 데이터 추가/삭제/수정이 가능한 지 판별 후 기능 활성화/비활성화"""
        date_send = self.sender()
        date_str = date_send.date().toString('yyyy-MM-dd')
        weekday = date_send.date().dayOfWeek()
        possible = True
        table = None
        date_label = None
        btn = None
        set_text = None
        label_list = list()
        spin_list = list()

        if date_send == self.kosdaq_date_add:
            self.kosdaq_group_add.setEnabled(False)
            self.kosdaq_btn_add.setEnabled(False)
            table = 'kosdaq'
            date_label = self.kosdaq_label_add
            btn = self.kosdaq_btn_addDate
            spin_list = [self.kosdaq_spin_add1, self.kosdaq_spin_add2, self.kosdaq_spin_add3,
                         self.kosdaq_spin_add4, self.kosdaq_spin_add5, self.kosdaq_spin_add6]
            set_text = '추가'
        if date_send == self.kosdaq_date_del:
            self.kosdaq_group_del.setEnabled(False)
            self.kosdaq_btn_del.setEnabled(False)
            table = 'kosdaq'
            date_label = self.kosdaq_label_del
            btn = self.kosdaq_btn_delDate
            spin_list = [self.kosdaq_spin_add1, self.kosdaq_spin_add2, self.kosdaq_spin_add3,
                         self.kosdaq_spin_add4, self.kosdaq_spin_add5, self.kosdaq_spin_add6]
            set_text = '삭제'
        if date_send == self.kosdaq_date_edit:
            self.kosdaq_group_edit.setEnabled(False)
            self.kosdaq_btn_edit.setEnabled(False)
            table = 'kosdaq'
            date_label = self.kosdaq_label_edit
            btn = self.kosdaq_btn_editDate
            set_text = '수정'

        if date_send == self.covering_date_add:
            self.covering_group_add.setEnabled(False)
            self.covering_btn_add.setEnabled(False)
            table = 'covering'
            date_label = self.covering_label_add
            btn = self.covering_btn_addDate
            set_text = '추가'
        if date_send == self.covering_date_del:
            self.covering_group_del.setEnabled(False)
            self.covering_btn_del.setEnabled(False)
            table = 'covering'
            date_label = self.covering_label_del
            btn = self.covering_btn_delDate
            set_text = '삭제'
        if date_send == self.covering_date_edit:
            self.covering_group_edit.setEnabled(False)
            self.covering_btn_edit.setEnabled(False)
            table = 'covering'
            date_label = self.covering_label_edit
            btn = self.covering_btn_editDate
            set_text = '수정'

        if date_send == self.baserate_date_add:
            self.baserate_group_add.setEnabled(False)
            self.baserate_btn_add.setEnabled(False)
            table = 'baserate'
            date_label = self.baserate_label_add
            btn = self.baserate_btn_addDate
            set_text = '추가'
        if date_send == self.baserate_date_del:
            self.baserate_group_del.setEnabled(False)
            self.baserate_btn_del.setEnabled(False)
            table = 'baserate'
            date_label = self.baserate_label_del
            btn = self.baserate_btn_delDate
            set_text = '삭제'
        if date_send == self.baserate_date_edit:
            self.baserate_group_edit.setEnabled(False)
            self.baserate_btn_edit.setEnabled(False)
            table = 'baserate'
            date_label = self.baserate_label_edit
            btn = self.baserate_btn_editDate
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
                        if set_text == '추가':
                            print(f"{set_text} - 데이터 존재")
                            date_label.setText("해당 날짜에 이미 데이터가 존재함")
                            btn.setEnabled(False)
                        else:
                            print(f"{set_text} - 데이터 존재")
                            date_label.setText(f"데이터 {set_text} 가능")
                            btn.setEnabled(True)
                    else:
                        if set_text == '추가':
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
            self.kosdaq_btn_add.setEnabled(True)
            self.kosdaq_label_add.clear()
        if date_send == self.covering_btn_addDate:
            self.covering_group_add.setEnabled(True)
            self.covering_btn_add.setEnabled(True)
            self.covering_label_add.clear()
        if date_send == self.baserate_btn_addDate:
            self.baserate_group_add.setEnabled(True)
            self.baserate_btn_add.setEnabled(True)
            self.baserate_label_add.clear()

        if date_send == self.kosdaq_btn_delDate or date_send == self.kosdaq_btn_editDate \
                or date_send == self.covering_btn_delDate or date_send == self.covering_btn_editDate \
                or date_send == self.baserate_btn_delDate or date_send == self.baserate_btn_editDate:
            group = None
            table = None
            date_info = None
            btn = None
            spin_list = list()
            label_list = list()

            if date_send == self.kosdaq_btn_delDate:
                self.kosdaq_label_del.clear()
                group = self.kosdaq_group_del
                btn = self.kosdaq_btn_del
                date_info = self.kosdaq_date_del
                label_list = [self.kosdaq_label_del1, self.kosdaq_label_del2, self.kosdaq_label_del3,
                              self.kosdaq_label_del4, self.kosdaq_label_del5, self.kosdaq_label_del6]
                table = 'kosdaq'
            if date_send == self.kosdaq_btn_editDate:
                self.kosdaq_label_edit.clear()
                group = self.kosdaq_group_edit
                btn = self.kosdaq_btn_edit
                date_info = self.kosdaq_date_edit
                label_list = [self.kosdaq_label_edit1, self.kosdaq_label_edit2, self.kosdaq_label_edit3,
                              self.kosdaq_label_edit4, self.kosdaq_label_edit5, self.kosdaq_label_edit6]
                spin_list = [self.kosdaq_spin_edit1, self.kosdaq_spin_edit2, self.kosdaq_spin_edit3,
                             self.kosdaq_spin_edit4, self.kosdaq_spin_edit5, self.kosdaq_spin_edit6]
                table = 'kosdaq'

            if date_send == self.covering_btn_delDate:
                self.covering_label_del.clear()
                group = self.covering_group_del
                btn = self.covering_btn_del
                date_info = self.covering_date_del
                label_list = [self.covering_label_del1, self.covering_label_del2, self.covering_label_del3,
                              self.covering_label_del4, self.covering_label_del5, self.covering_label_del6]
                table = 'covering'
            if date_send == self.covering_btn_editDate:
                self.covering_label_edit.clear()
                group = self.covering_group_edit
                btn = self.covering_btn_edit
                date_info = self.covering_date_edit
                label_list = [self.covering_label_edit1, self.covering_label_edit2, self.covering_label_edit3,
                              self.covering_label_edit4, self.covering_label_edit5, self.covering_label_edit6]
                spin_list = [self.covering_spin_edit1, self.covering_spin_edit2, self.covering_spin_edit3,
                             self.covering_spin_edit4, self.covering_spin_edit5, self.covering_spin_edit6]
                table = 'covering'

            if date_send == self.baserate_btn_delDate:
                self.baserate_label_del.clear()
                group = self.baserate_group_del
                btn = self.baserate_btn_del
                date_info = self.baserate_date_del
                label_list = [self.baserate_label_del1]
                table = 'baserate'
            if date_send == self.baserate_btn_editDate:
                self.baserate_label_edit.clear()
                group = self.baserate_group_edit
                btn = self.baserate_btn_edit
                date_info = self.baserate_date_edit
                label_list = [self.baserate_label_edit1]
                spin_list = [self.baserate_spin_edit1]
                table = 'baserate'

            group.setEnabled(True)
            btn.setEnabled(True)
            date_str = date_info.date().toString('yyyy-MM-dd')
            sql = f"SELECT * FROM {table} WHERE 날짜 = '{date_str}'"
            print(sql)

            con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
            cur = con.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            for i in rows:
                print(rows)
                for j in range(1, len(label_list) + 1):
                    print(j, end=' ')
                    label_list[j - 1].setText(str(i[j]))
                print()
            con.close()

            for i in range(len(spin_list)):
                if type(spin_list[i]) == QDoubleSpinBox:
                    spin_list[i].setValue(float(label_list[i].text()))
                if type(spin_list[i]) == QSpinBox:
                    spin_list[i].setValue(int(label_list[i].text()))

    def table_search(self):
        btn_send = self.sender()
        table = None
        table_widget = None
        date_before = None
        date_after = None
        label = None

        if btn_send == self.kosdaq_btn_search:
            table = 'kosdaq'
            table_widget = self.kosdaq_table
            date_before = self.kosdaq_date_before
            date_after = self.kosdaq_date_after
            label = self.kosdaq_label_impossible

        if btn_send == self.covering_btn_search:
            table = 'covering'
            table_widget = self.covering_table
            date_before = self.covering_date_before
            date_after = self.covering_date_after
            label = self.covering_label_impossible

        if btn_send == self.baserate_btn_search:
            table = 'baserate'
            table_widget = self.baserate_table
            date_before = self.baserate_date_before
            date_after = self.baserate_date_after
            label = self.baserate_label_impossible

        label.setVisible(False)
        table_widget.setRowCount(0)
        date_str1 = date_before.date().toString('yyyy-MM-dd')
        date_str2 = date_after.date().toString('yyyy-MM-dd')
        sql = f"SELECT * FROM {table} WHERE 날짜 BETWEEN '{date_str1}' and '{date_str2}' ORDER BY 날짜 DESC"
        print(sql)

        con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
        with con:
            with con.cursor() as cur:
                cur.execute(sql)
                result = cur.fetchall()
                row = 0
                col = 0
                table_widget.setRowCount(len(result))
                for i in result:
                    for j in i:
                        print(j, end='  ')
                        table_widget.setItem(col, row, QTableWidgetItem(str(j)))
                        row += 1
                    row = 0
                    col += 1
                    print()

    def add_data(self):
        btn_send = self.sender()
        table = None
        group = None
        btn = list()
        add_list = list()
        spin_list = list()
        col_list = list()

        if btn_send == self.kosdaq_btn_add:
            add_list = [self.kosdaq_date_add.date().toString('yyyy-MM-dd')]
            spin_list = [self.kosdaq_spin_add1, self.kosdaq_spin_add2, self.kosdaq_spin_add3,
                         self.kosdaq_spin_add4, self.kosdaq_spin_add5, self.kosdaq_spin_add6]
            col_list = '날짜, KOSDAQ지수, 거래량, 거래대금, 시가총액, 외국인_시가총액, 외국인_비중'
            group = self.kosdaq_group_add
            btn = [self.kosdaq_btn_add, self.kosdaq_btn_addDate]
            table = 'kosdaq'
        if btn_send == self.covering_btn_add:
            add_list = [self.covering_date_add.date().toString('yyyy-MM-dd')]
            spin_list = [self.covering_spin_add1, self.covering_spin_add2, self.covering_spin_add3,
                         self.covering_spin_add4, self.covering_spin_add5, self.covering_spin_add6]
            col_list = '날짜, 예탁금, 예수금, 매도잔고, 미수금, 반대매매금액, 반대매매비중'
            group = self.covering_group_add
            btn = [self.covering_btn_add, self.covering_btn_addDate]
            table = 'covering'
        if btn_send == self.baserate_btn_add:
            add_list = [self.baserate_date_add.date().toString('yyyy-MM-dd')]
            spin_list = [self.baserate_spin_add1]
            col_list = '날짜, 금리'
            group = self.baserate_group_add
            btn = [self.baserate_btn_add, self.baserate_btn_addDate]
            table = 'baserate'

        for i in spin_list:
            add_list.append(i.value())
        print(add_list)

        for i in add_list:
            if i == 0:
                QMessageBox.warning(self, '경고', '전부 입력 바람')
                return

        reply = QMessageBox.question(self, '확인', f'{add_list[0]} 날짜에 데이터를 추가하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.No:
            return

        sql = f"INSERT INTO {table} ({col_list}) VALUES ({str(add_list).lstrip('[').rstrip(']')})"
        print(sql)

        con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
        with con:
            with con.cursor() as cur:
                cur.execute(sql)
                con.commit()
                QMessageBox.information(self, '완료', '데이터가 추가되었습니다', QMessageBox.Apply)
                group.setEnabled(False)
                for i in btn:
                    i.setEnabled(False)
                for i in spin_list:
                    i.setValue(0)

    def del_data(self):
        btn_send = self.sender()
        table = None
        group = None
        del_date = None
        label_list = list()
        btn = list()

        if btn_send == self.kosdaq_btn_del:
            del_date = self.kosdaq_date_del.date().toString('yyyy-MM-dd')
            group = self.kosdaq_group_del
            label_list = [self.kosdaq_label_del1, self.kosdaq_label_del2, self.kosdaq_label_del3,
                          self.kosdaq_label_del4, self.kosdaq_label_del5, self.kosdaq_label_del6]
            btn = [self.kosdaq_btn_del, self.kosdaq_btn_delDate]
            table = 'kosdaq'
        if btn_send == self.covering_btn_del:
            del_date = self.covering_date_del.date().toString('yyyy-MM-dd')
            group = self.covering_group_del
            label_list = [self.covering_label_del1, self.covering_label_del2, self.covering_label_del3,
                          self.covering_label_del4, self.covering_label_del5, self.covering_label_del6]
            btn = [self.covering_btn_del, self.covering_btn_delDate]
            table = 'covering'
        if btn_send == self.baserate_btn_del:
            del_date = self.baserate_date_del.date().toString('yyyy-MM-dd')
            group = self.baserate_group_del
            label_list = [self.baserate_label_del1]
            btn = [self.baserate_btn_del, self.baserate_btn_delDate]
            table = 'baserate'

        reply = QMessageBox.question(self, '확인', f'{del_date} 날짜의 데이터를 삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.No:
            return

        sql = f"DELETE FROM {table} WHERE 날짜 = '{del_date}'"
        print(sql)

        con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
        with con:
            with con.cursor() as cur:
                cur.execute(sql)
                con.commit()
                QMessageBox.information(self, '완료', '데이터가 삭제되었습니다', QMessageBox.Apply)
                group.setEnabled(False)
                for i in btn:
                    i.setEnabled(False)
                for i in label_list:
                    i.clear()

    def edit_data(self):
        btn_send = self.sender()
        table = None
        group = None
        btn = list()
        edit_list = list()
        spin_list = list()
        label_list = list()
        col_list = list()

        if btn_send == self.kosdaq_btn_edit:
            edit_list = [self.kosdaq_date_edit.date().toString('yyyy-MM-dd')]
            spin_list = [self.kosdaq_spin_edit1, self.kosdaq_spin_edit2, self.kosdaq_spin_edit3,
                         self.kosdaq_spin_edit4, self.kosdaq_spin_edit5, self.kosdaq_spin_edit6]
            col_list = ['날짜', 'KOSDAQ지수', '거래량', '거래대금', '시가총액', '외국인_시가총액', '외국인_비중']
            label_list = [self.kosdaq_label_edit1, self.kosdaq_label_edit2, self.kosdaq_label_edit3,
                          self.kosdaq_label_edit4, self.kosdaq_label_edit5, self.kosdaq_label_edit6]
            group = self.kosdaq_group_edit
            btn = [self.kosdaq_btn_edit, self.kosdaq_btn_editDate]
            table = 'kosdaq'
        if btn_send == self.covering_btn_edit:
            edit_list = [self.covering_date_edit.date().toString('yyyy-MM-dd')]
            spin_list = [self.covering_spin_edit1, self.covering_spin_edit2, self.covering_spin_edit3,
                         self.covering_spin_edit4, self.covering_spin_edit5, self.covering_spin_edit6]
            col_list = ['날짜', '예탁금', '예수금', '매도잔고', '미수금', '반대매매금액', '반대매매비중']
            label_list = [self.covering_label_edit1, self.covering_label_edit2, self.covering_label_edit3,
                          self.covering_label_edit4, self.covering_label_edit5, self.covering_label_edit6]
            group = self.covering_group_edit
            btn = [self.covering_btn_edit, self.covering_btn_editDate]
            table = 'covering'
        if btn_send == self.baserate_btn_edit:
            edit_list = [self.baserate_date_edit.date().toString('yyyy-MM-dd')]
            spin_list = [self.baserate_spin_edit1]
            col_list = ['날짜', '금리']
            label_list = [self.baserate_label_edit1]
            group = self.baserate_group_edit
            btn = [self.baserate_btn_edit, self.baserate_btn_editDate]
            table = 'baserate'

        for i in spin_list:
            edit_list.append(i.value())
        print(edit_list)

        for i in edit_list:
            if i == 0:
                QMessageBox.warning(self, '경고', '전부 입력 바람')
                return

        reply = QMessageBox.question(self, '확인', f'{edit_list[0]} 날짜에 데이터를 추가하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.No:
            return

        sql = f"UPDATE {table} SET "
        for i in range(1, len(edit_list)):
            sql += f"{col_list[i]} = {edit_list[i]}"
            if i != len(edit_list) - 1:
                sql += ", "
        sql += f" WHERE {col_list[0]} = '{edit_list[0]}'"
        print(sql)

        con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
        with con:
            with con.cursor() as cur:
                cur.execute(sql)
                con.commit()
                QMessageBox.information(self, '완료', '데이터가 수정되었습니다', QMessageBox.Apply)
                group.setEnabled(False)
                for i in btn:
                    i.setEnabled(False)
                for i in label_list:
                    i.clear()
                for i in spin_list:
                    i.setValue(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
