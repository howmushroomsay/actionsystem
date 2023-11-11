# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(1920, 1080)
        self.lab_camera = QtWidgets.QLabel(Login)
        self.lab_camera.setGeometry(QtCore.QRect(860, 430, 200, 200))
        self.lab_camera.setMinimumSize(QtCore.QSize(200, 200))
        self.lab_camera.setMaximumSize(QtCore.QSize(200, 200))
        self.lab_camera.setStyleSheet("")
        self.lab_camera.setLineWidth(0)
        self.lab_camera.setText("")
        self.lab_camera.setPixmap(QtGui.QPixmap(":/icons/figs/icon/log_user.png"))
        self.lab_camera.setObjectName("lab_camera")
        self.text_welcome = QtWidgets.QLabel(Login)
        self.text_welcome.setGeometry(QtCore.QRect(785, 300, 350, 100))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(42)
        font.setBold(True)
        font.setWeight(75)
        self.text_welcome.setFont(font)
        self.text_welcome.setStyleSheet("color: rgb(255, 255, 255);")
        self.text_welcome.setLineWidth(0)
        self.text_welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.text_welcome.setObjectName("text_welcome")
        self.log_opt = QtWidgets.QFrame(Login)
        self.log_opt.setGeometry(QtCore.QRect(760, 670, 400, 50))
        self.log_opt.setStyleSheet("QPushButton{\n"
"  border:none;\n"
"  color:rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
" padding-bottom:4px;\n"
"}\n"
"")
        self.log_opt.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.log_opt.setFrameShadow(QtWidgets.QFrame.Raised)
        self.log_opt.setObjectName("log_opt")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.log_opt)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_open = QtWidgets.QPushButton(self.log_opt)
        self.btn_open.setMinimumSize(QtCore.QSize(180, 40))
        self.btn_open.setMaximumSize(QtCore.QSize(180, 40))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.btn_open.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/figs/icon/相机.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_open.setIcon(icon)
        self.btn_open.setIconSize(QtCore.QSize(30, 30))
        self.btn_open.setObjectName("btn_open")
        self.horizontalLayout.addWidget(self.btn_open)
        self.btn_close = QtWidgets.QPushButton(self.log_opt)
        self.btn_close.setEnabled(True)
        self.btn_close.setMinimumSize(QtCore.QSize(180, 40))
        self.btn_close.setMaximumSize(QtCore.QSize(180, 40))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.btn_close.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/figs/icon/退出.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_close.setIcon(icon1)
        self.btn_close.setIconSize(QtCore.QSize(30, 30))
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout.addWidget(self.btn_close)
        self.logo = QtWidgets.QPushButton(Login)
        self.logo.setGeometry(QtCore.QRect(50, 20, 450, 80))
        self.logo.setMinimumSize(QtCore.QSize(450, 80))
        self.logo.setMaximumSize(QtCore.QSize(450, 80))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(24)
        self.logo.setFont(font)
        self.logo.setStyleSheet("border:none;\n"
"color: rgb(255, 255, 255);")
        self.logo.setIconSize(QtCore.QSize(30, 30))
        self.logo.setObjectName("logo")

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Form"))
        self.text_welcome.setText(_translate("Login", "欢迎登录"))
        self.btn_open.setText(_translate("Login", "打开相机"))
        self.btn_close.setText(_translate("Login", "退出登录"))
        self.logo.setText(_translate("Login", "警察动作评估训练系统 | 测试版"))
import res_rc
