import pymysql
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("main.ui")[0]


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        con = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock', charset='utf8')
        cur = con.cursor()
        sql = "SELECT * FROM covering"
        cur.execute(sql)
        rows = cur.fetchall()
        label_str = ''
        cnt1 = 0
        cnt2 = 0
        self.tableWidget.setRowCount(len(rows))
        for i in rows:
            for j in i:
                print(j, end='  ')
                self.tableWidget.setItem(cnt1, cnt2, QTableWidgetItem(str(j)))
                cnt2 += 1
            cnt2 = 0
            cnt1 += 1
            print()

                # label_str += str(j)+', '
        # label_str_list = label_str.split(', ')
        # self.tableWidget.setRowCount(5)
        # self.tableWidget.setItem(0, 0, QTableWidgetItem(label_str_list[0]))
        # self.tableWidget.setItem(0, 1, QTableWidgetItem(label_str_list[1]))
        # self.tableWidget.setItem(0, 2, QTableWidgetItem(label_str_list[2]))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.label.setText(label_str)
        # print(rows
        con.close()


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()


# con = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock', charset='utf8')
# cur = con.cursor()
# sql = "SELECT * FROM covering where `날짜`='2020-01-02'"
# cur.execute(sql)
# rows = cur.fetchall()
# for i in rows:
#     print(i)
# # print(rows)
# con.close()
