# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\user\Desktop\project\actionsystem\widgets\ui\Grade_reaction.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Grade_reaction(object):
    def setupUi(self, Grade_reaction):
        Grade_reaction.setObjectName("Grade_reaction")
        Grade_reaction.resize(1920, 1080)
        Grade_reaction.setStyleSheet("background-color: rgb(8, 60, 121)")
        self.lab_title = QtWidgets.QLabel(Grade_reaction)
        self.lab_title.setGeometry(QtCore.QRect(0, -60, 2081, 251))
        self.lab_title.setText("")
        self.lab_title.setPixmap(QtGui.QPixmap("c:\\Users\\user\\Desktop\\project\\actionsystem\\widgets\\ui\\../../../../../Documents/WeChat Files/wxid_t3txe9xn4ovz21/data/icons/头部5.png"))
        self.lab_title.setObjectName("lab_title")
        self.tableWidget = QtWidgets.QTableWidget(Grade_reaction)
        self.tableWidget.setGeometry(QtCore.QRect(170, 180, 1571, 801))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("alternate-background-color: rgb(80, 97, 139);\n"
"pane{border: -3px;top:-3px;left: 3px;};\n"
"background-color: rgb(23, 56, 108);\n"
"border-width: 1px;\n"
"border-style: solid;\n"
"border-color: rgb(255, 255, 255);\n"
"color: rgb(255, 255, 255);")
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(24)
        item.setFont(font)
        item.setBackground(QtGui.QColor(0, 0, 0))
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(24)
        item.setFont(font)
        item.setBackground(QtGui.QColor(0, 0, 0))
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(24)
        item.setFont(font)
        item.setBackground(QtGui.QColor(0, 0, 0))
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(24)
        item.setFont(font)
        item.setBackground(QtGui.QColor(0, 0, 0))
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(30)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.btn_back = QtWidgets.QPushButton(Grade_reaction)
        self.btn_back.setGeometry(QtCore.QRect(840, 1010, 261, 51))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.btn_back.setFont(font)
        self.btn_back.setStyleSheet("border:1px solid rgb(255, 255, 255);\n"
"color: rgb(255, 255, 255);")
        self.btn_back.setObjectName("btn_back")
        self.label = QtWidgets.QLabel(Grade_reaction)
        self.label.setGeometry(QtCore.QRect(800, 70, 320, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(24)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color:rgb(255, 255, 255);\n"
"background-color:transparent;")
        self.label.setObjectName("label")

        self.retranslateUi(Grade_reaction)
        QtCore.QMetaObject.connectSlotsByName(Grade_reaction)

    def retranslateUi(self, Grade_reaction):
        _translate = QtCore.QCoreApplication.translate
        Grade_reaction.setWindowTitle(_translate("Grade_reaction", "Form"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Grade_reaction", "课程名称"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Grade_reaction", "课程描述"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Grade_reaction", "训练时间"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Grade_reaction", "得分"))
        self.btn_back.setText(_translate("Grade_reaction", "退出成绩查询"))
        self.label.setText(_translate("Grade_reaction", "执法动作训练成绩查询"))
import res_rc
