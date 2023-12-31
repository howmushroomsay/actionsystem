# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\PoseUI\PoseUI\widgets\ui\reaction_train_playerP2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Reaction_Train_PlayerP2(object):
    def setupUi(self, Reaction_Train_PlayerP2):
        Reaction_Train_PlayerP2.setObjectName("Reaction_Train_PlayerP2")
        Reaction_Train_PlayerP2.resize(1920, 1080)
        self.contrl_frame = QtWidgets.QFrame(Reaction_Train_PlayerP2)
        self.contrl_frame.setGeometry(QtCore.QRect(0, 930, 1920, 150))
        self.contrl_frame.setMinimumSize(QtCore.QSize(1920, 150))
        self.contrl_frame.setSizeIncrement(QtCore.QSize(1920, 150))
        self.contrl_frame.setStyleSheet("QFrame{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(0, 0, 0, 180), stop:1 rgba(100, 100, 100, 0));\n"
"}\n"
"")
        self.contrl_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.contrl_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.contrl_frame.setObjectName("contrl_frame")
        self.sld_video = QtWidgets.QSlider(self.contrl_frame)
        self.sld_video.setGeometry(QtCore.QRect(10, 30, 1900, 20))
        self.sld_video.setMinimumSize(QtCore.QSize(0, 20))
        self.sld_video.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.sld_video.setFont(font)
        self.sld_video.setStyleSheet("/*horizontal ：水平QSlider*/\n"
"QSlider{\n"
"    background-color: rgba(0, 0, 0,0);\n"
"}\n"
"QSlider::groove:horizontal {\n"
"border: 0px solid #bbb;\n"
"}\n"
"\n"
"/*1.滑动过的槽设计参数*/\n"
"QSlider::sub-page:horizontal {\n"
" /*槽颜色*/\n"
"background:rgb(66, 156, 227);\n"
" /*外环区域倒圆角度*/\n"
"border-radius: 2px;\n"
" /*上遮住区域高度*/\n"
"margin-top:8px;\n"
" /*下遮住区域高度*/\n"
"margin-bottom:8px;\n"
"/*width在这里无效，不写即可*/\n"
"}\n"
"\n"
"/*2.未滑动过的槽设计参数*/\n"
"QSlider::add-page:horizontal {\n"
"/*槽颜色*/\n"
"background: rgba(255,255, 255, 100);\n"
"/*外环大小0px就是不显示，默认也是0*/\n"
"border: 0px solid #777;\n"
"/*外环区域倒圆角度*/\n"
"border-radius: 2px;\n"
" /*上遮住区域高度*/\n"
"margin-top:8px;\n"
" /*下遮住区域高度*/\n"
"margin-bottom:9px;\n"
"}\n"
" \n"
"/*3.平时滑动的滑块设计参数*/\n"
"QSlider::handle:horizontal {\n"
"/*滑块颜色*/\n"
"background: rgb(193,204,208);\n"
"/*滑块的宽度*/\n"
"width: 5px;\n"
"/*滑块外环为1px，再加颜色*/\n"
"border: 1px solid rgb(193,204,208);\n"
" /*滑块外环倒圆角度*/\n"
"border-radius: 2px; \n"
" /*上遮住区域高度*/\n"
"margin-top:6px;\n"
" /*下遮住区域高度*/\n"
"margin-bottom:6px;\n"
"}\n"
"\n"
"/*4.手动拉动时显示的滑块设计参数*/\n"
"QSlider::handle:horizontal:hover {\n"
"/*滑块颜色*/\n"
"background: rgb(193,204,208);\n"
"/*滑块的宽度*/\n"
"width: 10px;\n"
"/*滑块外环为1px，再加颜色*/\n"
"border: 1px solid rgb(193,204,208);\n"
" /*滑块外环倒圆角度*/\n"
"border-radius: 5px; \n"
" /*上遮住区域高度*/\n"
"margin-top:4px;\n"
" /*下遮住区域高度*/\n"
"margin-bottom:4px;\n"
"}\n"
"")
        self.sld_video.setOrientation(QtCore.Qt.Horizontal)
        self.sld_video.setObjectName("sld_video")
        self.btn_playorstop = QtWidgets.QPushButton(self.contrl_frame)
        self.btn_playorstop.setGeometry(QtCore.QRect(940, 70, 40, 40))
        self.btn_playorstop.setStyleSheet("QPushButton{\n"
"border:none;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:none;\n"
"background-color: rgba(255, 255, 255, 50);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"border:none;\n"
"}")
        self.btn_playorstop.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/figs/icon/24gl-pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_playorstop.setIcon(icon)
        self.btn_playorstop.setIconSize(QtCore.QSize(25, 25))
        self.btn_playorstop.setObjectName("btn_playorstop")
        self.btn_exit = QtWidgets.QPushButton(self.contrl_frame)
        self.btn_exit.setGeometry(QtCore.QRect(1800, 70, 40, 40))
        self.btn_exit.setStyleSheet("QPushButton{\n"
"border:none;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:none;\n"
"background-color: rgba(255, 255, 255, 50);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"border:none;\n"
"}")
        self.btn_exit.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/figs/icon/退出.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_exit.setIcon(icon1)
        self.btn_exit.setIconSize(QtCore.QSize(25, 25))
        self.btn_exit.setObjectName("btn_exit")
        self.lab_time = QtWidgets.QLabel(self.contrl_frame)
        self.lab_time.setGeometry(QtCore.QRect(10, 50, 120, 25))
        self.lab_time.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lab_time.setFont(font)
        self.lab_time.setStyleSheet("color: rgba(255, 255, 255,200);\n"
"background-color: rgba(255, 255, 255,0);")
        self.lab_time.setObjectName("lab_time")

        self.retranslateUi(Reaction_Train_PlayerP2)
        QtCore.QMetaObject.connectSlotsByName(Reaction_Train_PlayerP2)

    def retranslateUi(self, Reaction_Train_PlayerP2):
        _translate = QtCore.QCoreApplication.translate
        Reaction_Train_PlayerP2.setWindowTitle(_translate("Reaction_Train_PlayerP2", "Form"))
        self.lab_time.setText(_translate("Reaction_Train_PlayerP2", "00:00:00/00:00:00"))
import res_rc
