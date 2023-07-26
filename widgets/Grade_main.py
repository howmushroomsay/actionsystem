import sys,os, cv2

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QHeaderView, QAbstractItemView
from PyQt5 import QtCore, QtGui, QtWidgets


# from .ui import Ui_Grade
from .ui import Ui_Grade_std, Ui_Grade_reaction

class Grade_std(QWidget, Ui_Grade_std):
    def __init__(self, parent, db, student_id):
        super(Grade_std, self).__init__()
        self.parent = parent
        self.db = db
        self.student_id = student_id
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.tableWidget.horizontalHeader().setStyleSheet(
    "QHeaderView::section{background-color:rgb(0, 0, 0);font:24pt '微软雅黑';color: (150, 150, 255);};")
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeToContents)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(4,QHeaderView.ResizeToContents)
        self.show_grade()
        self.btn_back.clicked.connect(self.back)
    
    def show_grade(self):
        sql_grade = """SELECT course_name, action_Name, action_Description, grade, train_time FROM grade_std
                        JOIN action_info
                        ON action_info.action_ID = grade_std.action_ID
                        JOIN course_standard
                        ON course_standard.course_ID = action_info.course_ID
                        WHERE student_id={}""".format(self.student_id)
        
        data = self.db.search_table(sql_grade)
        self.tableWidget.setRowCount(len(data))
        for i in range(len(data)):
            course_name_Item = QtWidgets.QTableWidgetItem(data[i][0])
            action_Name_Item = QtWidgets.QTableWidgetItem(data[i][1])
            action_Des_Item = QtWidgets.QTableWidgetItem(data[i][2])
            grade_Item = QtWidgets.QTableWidgetItem(data[i][3])
            time_Item = QtWidgets.QTableWidgetItem(data[i][4].strftime("%Y.%m.%d.%H:%M"))
            self.tableWidget.setItem(i, 0, course_name_Item)
            self.tableWidget.setItem(i, 1, action_Name_Item)
            self.tableWidget.setItem(i, 2, action_Des_Item)
            self.tableWidget.setItem(i, 3, time_Item)
            self.tableWidget.setItem(i, 4, grade_Item)
        for i in range(len(data)):
            for j in range(5):
                self.tableWidget.item(i,j).setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    def back(self):
        self.parent.show()
        self.close()

class Grade_reaction(QWidget, Ui_Grade_reaction):
    def __init__(self, parent, db, student_id):
        super(Grade_reaction, self).__init__()
        self.parent = parent
        self.db = db
        self.student_id = student_id
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.tableWidget.horizontalHeader().setStyleSheet(
    "QHeaderView::section{background-color:rgb(0, 0, 0);font:24pt '微软雅黑';color: (150, 150, 255);};")
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeToContents)
        self.show_grade()
        self.btn_back.clicked.connect(self.back)
    
    def show_grade(self):
        sql_grade = """SELECT course_name, course_Description, grade, train_time FROM grade_reaction
                        JOIN course_actionresponse
                        ON course_actionresponse.course_ID = grade_reaction.course_ID
                        WHERE student_id={}""".format(self.student_id)
        data = self.db.search_table(sql_grade)
        self.tableWidget.setRowCount(len(data))
        for i in range(len(data)):
            course_name_Item = QtWidgets.QTableWidgetItem(data[i][0])
            course_Des_Item = QtWidgets.QTableWidgetItem(data[i][1])
            grade_Item = QtWidgets.QTableWidgetItem(data[i][2])
            time_Item = QtWidgets.QTableWidgetItem(data[i][3].strftime("%Y.%m.%d.%H:%M"))
            self.tableWidget.setItem(i, 0, course_name_Item)
            self.tableWidget.setItem(i, 1, course_Des_Item)
            self.tableWidget.setItem(i, 2, time_Item)
            self.tableWidget.setItem(i, 3, grade_Item)
        for i in range(len(data)):
            for j in range(4):
                self.tableWidget.item(i,j).setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    def back(self):
        self.parent.show()
        self.close()
# class Grade_Main(QWidget, Ui_Grade):
#     def __init__(self, parent, db, student_id, is_Standard):
#         super(Grade_Main, self).__init__()
#         self.parent = parent
#         self.db = db
#         self.student_id = student_id
#         self.is_Standard = is_Standard
#         self.setupUi(self)
#         self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
#         self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         self.tableWidget.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)
#         self.tableWidget.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeToContents)
#         # self.tableWidget.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeToContents)
#         self.tableWidget.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeToContents)
#         self.tableWidget.horizontalHeader().setSectionResizeMode(4,QHeaderView.ResizeToContents)
#         self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         self.tableWidget.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)
#         # self.tableWidget.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeToContents)
#         self.tableWidget.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeToContents)
#         self.tableWidget.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeToContents)
#         self.show_grade()
#         self.btn_back.clicked.connect(self.back)
#     def show_grade(self):
#         sql_grade = """SELECT course_name, action_Name, action_Description, grade, train_time FROM grade_std
#                         JOIN action_info
#                         ON action_info.action_ID = grade_std.action_ID
#                         JOIN course_standard
#                         ON course_standard.course_ID = action_info.course_ID
#                         WHERE student_id={}""".format(self.student_id)
        
#         data = self.db.search_table(sql_grade)
#         self.tableWidget.setRowCount(len(data))

#         for i in range(len(data)):
#             course_name_Item = QtWidgets.QTableWidgetItem(data[i][0])
#             action_Name_Item = QtWidgets.QTableWidgetItem(data[i][1])
#             action_Des_Item = QtWidgets.QTableWidgetItem(data[i][2])
#             grade_Item = QtWidgets.QTableWidgetItem(data[i][3])
#             time_Item = QtWidgets.QTableWidgetItem(data[i][4].strftime("%Y.%m.%d.%H:%M"))
#             self.tableWidget.setItem(i, 0, course_name_Item)
#             self.tableWidget.setItem(i, 1, action_Name_Item)
#             self.tableWidget.setItem(i, 2, action_Des_Item)
#             self.tableWidget.setItem(i, 3, time_Item)
#             self.tableWidget.setItem(i, 4, grade_Item)
#         for i in range(len(data)):
#             for j in range(5):
#                 self.tableWidget.item(i,j).setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
#         # sql_grade = """SELECT course_name, grade, train_time FROM grade_reaction
#         #                 JOIN course_actionresponse
#         #                 ON course_actionresponse.course_ID = grade_reaction.course_ID
#         #                 WHERE student_id={}""".format(self.student_id)
#         sql_grade = """SELECT course_name, course_Description, grade, train_time FROM grade_reaction
#                         JOIN course_actionresponse
#                         ON course_actionresponse.course_ID = grade_reaction.course_ID
#                         WHERE student_id={}""".format(self.student_id)
#         data = self.db.search_table(sql_grade)
#         self.tableWidget.setRowCount(len(data))
#         for i in range(len(data)):
#             course_name_Item = QtWidgets.QTableWidgetItem(data[i][0])
#             course_Des_Item = QtWidgets.QTableWidgetItem(data[i][1])
#             grade_Item = QtWidgets.QTableWidgetItem(data[i][2])
#             time_Item = QtWidgets.QTableWidgetItem(data[i][3].strftime("%Y.%m.%d.%H:%M"))
#             self.tableWidget.setItem(i, 0, course_name_Item)
#             self.tableWidget.setItem(i, 1, course_Des_Item)
#             self.tableWidget.setItem(i, 2, time_Item)
#             self.tableWidget.setItem(i, 3, grade_Item)
#         for i in range(len(data)):
#             for j in range(4):
#                 self.tableWidget.item(i,j).setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
#     def back(self):
#         self.parent.show()
#         self.close()