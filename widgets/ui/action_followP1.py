# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\user\Desktop\PoseUI\widgets\ui\action_followP1.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Action_FollowP1(object):
    def setupUi(self, Action_FollowP1):
        Action_FollowP1.setObjectName("Action_FollowP1")
        Action_FollowP1.resize(1920, 1080)
        self.videoWidget = QVideoWidget(Action_FollowP1)
        self.videoWidget.setGeometry(QtCore.QRect(0, 80, 1920, 1000))
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
        font.setWeight(50)
        self.lab_tip.setFont(font)
        self.lab_tip.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);\n"
"font: 36pt \"黑体\";")
        self.lab_tip.setScaledContents(False)
        self.lab_tip.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_tip.setObjectName("lab_tip")
        self.verticalLayout.addWidget(self.lab_tip)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.label = QtWidgets.QLabel(Action_FollowP1)
        self.label.setGeometry(QtCore.QRect(0, 0, 1920, 80))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/background/figs/background/头部5.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(Action_FollowP1)
        QtCore.QMetaObject.connectSlotsByName(Action_FollowP1)

    def retranslateUi(self, Action_FollowP1):
        _translate = QtCore.QCoreApplication.translate
        Action_FollowP1.setWindowTitle(_translate("Action_FollowP1", "Form"))
        self.lab_tip.setText(_translate("Action_FollowP1", "准备！"))
from PyQt5.QtMultimediaWidgets import QVideoWidget
import res_rc