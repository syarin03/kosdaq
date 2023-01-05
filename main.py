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
        self.tab_search.setCurrentWidget(self.kosdaq_tab_search)
        self.tab_manage.setCurrentWidget(self.kosdaq_tab)
        self.kosdaq_tab_manage.setCurrentWidget(self.kosdaq_tab_add)
        self.covering_tab_manage.setCurrentWidget(self.covering_tab_add)
        self.baserate_tab_manage.setCurrentWidget(self.baserate_tab_add)

        self.kosdaq_label_impossible.setVisible(False)
        self.covering_label_impossible.setVisible(False)
        self.baserate_label_impossible.setVisible(False)

        self.kosdaq_date_add.setDate(QDate.currentDate())
        self.kosdaq_date_del.setDate(QDate.currentDate())
        self.kosdaq_date_edit.setDate(QDate.currentDate())
        self.covering_date_add.setDate(QDate.currentDate())
        self.covering_date_del.setDate(QDate.currentDate())
        self.covering_date_edit.setDate(QDate.currentDate())
        self.baserate_date_add.setDate(QDate.currentDate())
        self.baserate_date_del.setDate(QDate.currentDate())
        self.baserate_date_edit.setDate(QDate.currentDate())
        self.kosdaq_date_add.setMaximumDate(QDate.currentDate())
        self.kosdaq_date_del.setMaximumDate(QDate.currentDate())
        self.kosdaq_date_edit.setMaximumDate(QDate.currentDate())
        self.covering_date_add.setMaximumDate(QDate.currentDate())
        self.covering_date_del.setMaximumDate(QDate.currentDate())
        self.covering_date_edit.setMaximumDate(QDate.currentDate())
        self.baserate_date_add.setMaximumDate(QDate.currentDate())
        self.baserate_date_del.setMaximumDate(QDate.currentDate())
        self.baserate_date_edit.setMaximumDate(QDate.currentDate())
        self.set_date_minimum()
        self.kosdaq_date_after.setDate(QDate.currentDate())
        self.kosdaq_date_before.setMaximumDate(QDate.currentDate())
        self.kosdaq_date_after.setMaximumDate(QDate.currentDate())
        self.covering_date_after.setDate(QDate.currentDate())
        self.covering_date_before.setMaximumDate(QDate.currentDate())
        self.covering_date_after.setMaximumDate(QDate.currentDate())
        self.baserate_date_after.setDate(QDate.currentDate())
        self.baserate_date_before.setMaximumDate(QDate.currentDate())
        self.baserate_date_after.setMaximumDate(QDate.currentDate())

        self.btn_go_manage.clicked.connect(self.go_manage)
        self.btn_go_search.clicked.connect(self.go_search)
        self.btn_search_to_main.clicked.connect(self.go_main)
        self.btn_manage_to_main.clicked.connect(self.go_main)
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

        self.tab_search.currentChanged.connect(self.reset_tab)
        self.tab_manage.currentChanged.connect(self.reset_tab)
        self.kosdaq_tab_manage.currentChanged.connect(self.reset_tab)
        self.covering_tab_manage.currentChanged.connect(self.reset_tab)
        self.baserate_tab_manage.currentChanged.connect(self.reset_tab)

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

    def go_main(self):
        self.stackedWidget.setCurrentWidget(self.stack_main)

    def go_manage(self):
        self.stackedWidget.setCurrentWidget(self.stack_manage)

    def go_search(self):
        self.stackedWidget.setCurrentWidget(self.stack_search)

    def reset_tab(self):
        self.kosdaq_table.setRowCount(0)
        self.covering_table.setRowCount(0)
        self.baserate_table.setRowCount(0)

        self.kosdaq_label_del1.setText('')
        self.kosdaq_label_del2.setText('')
        self.kosdaq_label_del3.setText('')
        self.kosdaq_label_del4.setText('')
        self.kosdaq_label_del5.setText('')
        self.kosdaq_label_del6.setText('')

        self.kosdaq_label_edit1.setText('')
        self.kosdaq_label_edit2.setText('')
        self.kosdaq_label_edit3.setText('')
        self.kosdaq_label_edit4.setText('')
        self.kosdaq_label_edit5.setText('')
        self.kosdaq_label_edit6.setText('')

        self.covering_label_del1.setText('')
        self.covering_label_del2.setText('')
        self.covering_label_del3.setText('')
        self.covering_label_del4.setText('')
        self.covering_label_del5.setText('')
        self.covering_label_del6.setText('')

        self.covering_label_edit1.setText('')
        self.covering_label_edit2.setText('')
        self.covering_label_edit3.setText('')
        self.covering_label_edit4.setText('')
        self.covering_label_edit5.setText('')
        self.covering_label_edit6.setText('')

        self.baserate_label_del1.setText('')

        self.baserate_label_edit1.setText('')

    def set_date(self):
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
        date_send = self.sender()
        date_str = date_send.date().toString('yyyy-MM-dd')
        weekday = date_send.date().dayOfWeek()
        possible = True
        table = None
        date_label = None
        btn = None
        set_text = None

        if date_send == self.kosdaq_date_add:
            self.kosdaq_group_add.setEnabled(False)
            self.kosdaq_btn_add.setEnabled(False)
            table = 'kosdaq'
            date_label = self.kosdaq_label_add
            btn = self.kosdaq_btn_addDate
            set_text = '추가'
        if date_send == self.kosdaq_date_del:
            self.kosdaq_group_del.setEnabled(False)
            self.kosdaq_btn_del.setEnabled(False)
            table = 'kosdaq'
            date_label = self.kosdaq_label_del
            btn = self.kosdaq_btn_delDate
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
        if date_send == self.covering_btn_addDate:
            self.covering_group_add.setEnabled(True)
            self.covering_btn_add.setEnabled(True)
        if date_send == self.baserate_btn_addDate:
            self.baserate_group_add.setEnabled(True)
            self.baserate_btn_add.setEnabled(True)

        if date_send == self.kosdaq_btn_delDate or date_send == self.kosdaq_btn_editDate \
                or date_send == self.covering_btn_delDate or date_send == self.covering_btn_editDate \
                or date_send == self.baserate_btn_delDate or date_send == self.baserate_btn_editDate:
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
            if date_send == self.kosdaq_btn_editDate:
                group = self.kosdaq_group_edit
                date_info = self.kosdaq_date_edit
                label_list = [self.kosdaq_label_edit1, self.kosdaq_label_edit2, self.kosdaq_label_edit3,
                              self.kosdaq_label_edit4, self.kosdaq_label_edit5, self.kosdaq_label_edit6]
                table = 'kosdaq'

            if date_send == self.covering_btn_delDate:
                group = self.covering_group_del
                date_info = self.covering_date_del
                label_list = [self.covering_label_del1, self.covering_label_del2, self.covering_label_del3,
                              self.covering_label_del4, self.covering_label_del5, self.covering_label_del6]
                table = 'covering'
            if date_send == self.covering_btn_editDate:
                group = self.covering_group_edit
                date_info = self.covering_date_edit
                label_list = [self.covering_label_edit1, self.covering_label_edit2, self.covering_label_edit3,
                              self.covering_label_edit4, self.covering_label_edit5, self.covering_label_edit6]
                table = 'covering'

            if date_send == self.baserate_btn_delDate:
                group = self.baserate_group_del
                date_info = self.baserate_date_del
                label_list = [self.baserate_label_del1]
                table = 'baserate'
            if date_send == self.baserate_btn_editDate:
                group = self.baserate_group_edit
                date_info = self.baserate_date_edit
                label_list = [self.baserate_label_edit1]
                table = 'baserate'

            group.setEnabled(True)
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
        add_list = list()
        col_list = list()

        if btn_send == self.kosdaq_btn_add:
            add_list = [self.kosdaq_date_add.date().toString('yyyy-MM-dd'),
                        self.kosdaq_spin_add1.value(), self.kosdaq_spin_add2.value(), self.kosdaq_spin_add3.value(),
                        self.kosdaq_spin_add4.value(), self.kosdaq_spin_add5.value(), self.kosdaq_spin_add6.value()]
            col_list = '날짜, KOSDAQ지수, 거래량, 거래대금, 시가총액, 외국인_시가총액, 외국인_비중'
            table = 'kosdaq'
        if btn_send == self.covering_btn_add:
            add_list = [self.covering_date_add.date().toString('yyyy-MM-dd'),
                        self.covering_spin_add1.value(), self.covering_spin_add2.value(), self.covering_spin_add3.value(),
                        self.covering_spin_add4.value(), self.covering_spin_add5.value(), self.covering_spin_add6.value()]
            col_list = '날짜, 예탁금, 예수금, 매도잔고, 미수금, 반대매매금액, 반대매매비중'
            table = 'covering'
        if btn_send == self.baserate_btn_add:
            add_list = [self.baserate_date_add.date().toString('yyyy-MM-dd'),
                        self.baserate_spin_add1.value()]
            col_list = '날짜, 금리'
            table = 'baserate'

        print(add_list)

        for i in add_list:
            if i == 0:
                QMessageBox.warning(self, '경고', '전부 입력 바람')
                return

        reply = QMessageBox.question(self, '확인', f'{add_list[0]} 날짜에 데이터를 추가하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        add_list = str(add_list).lstrip('[').rstrip(']')
        print(add_list)

        sql = f"INSERT INTO {table} ({col_list}) VALUES ({add_list})"
        print(sql)

        con = pymysql.connect(host=host_str, user=user_str, password=password_str, db='stock', charset='utf8')
        with con:
            with con.cursor() as cur:
                cur.execute(sql)
                con.commit()
                QMessageBox.information(self, '완료', '데이터가 추가되었습니다', QMessageBox.Apply)


    def del_data(self):
        btn_send = self.sender()

    def edit_data(self):
        btn_send = self.sender()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
