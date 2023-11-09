# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\user\Desktop\project\action_system\action_system\widgets\ui\followtest.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1920, 1080)
        Form.setStyleSheet("background-color: rgb(6,25,65);")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lab_cam = QtWidgets.QLabel(Form)
        self.lab_cam.setMinimumSize(QtCore.QSize(320, 320))
        self.lab_cam.setStyleSheet("background-color: rgba(85, 170, 255, 0);")
        self.lab_cam.setText("")
        self.lab_cam.setObjectName("lab_cam")
        self.verticalLayout_2.addWidget(self.lab_cam)
        self.lab_info = QtWidgets.QLabel(Form)
        self.lab_info.setMinimumSize(QtCore.QSize(320, 600))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(19)
        self.lab_info.setFont(font)
        self.lab_info.setStyleSheet("background-color: rgb(6,26,68);\n"
"border-color: rgb(255, 255, 127);\n"
"color: rgb(255, 255, 255);")
        self.lab_info.setText("")
        self.lab_info.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_info.setWordWrap(True)
        self.lab_info.setObjectName("lab_info")
        self.verticalLayout_2.addWidget(self.lab_info)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(1920, 80))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/background/figs/background/反应.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.videoWidget = QVideoWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoWidget.sizePolicy().hasHeightForWidth())
        self.videoWidget.setSizePolicy(sizePolicy)
        self.videoWidget.setObjectName("videoWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.videoWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lab_tip = QtWidgets.QLabel(self.videoWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lab_tip.sizePolicy().hasHeightForWidth())
        self.lab_tip.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        self.lab_tip.setFont(font)
        self.lab_tip.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);\n"
"font: 36pt \"黑体\";")
        self.lab_tip.setScaledContents(False)
        self.lab_tip.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_tip.setObjectName("lab_tip")
        self.verticalLayout.addWidget(self.lab_tip)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addWidget(self.videoWidget, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lab_tip.setText(_translate("Form", "准备！"))
from PyQt5.QtMultimediaWidgets import QVideoWidget
import res_rc
