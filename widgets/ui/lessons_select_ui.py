# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\user\Desktop\action\action\actionsystem\widgets\ui\lessons_select.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Lessons_Select(object):
    def setupUi(self, Lessons_Select):
        Lessons_Select.setObjectName("Lessons_Select")
        Lessons_Select.resize(1920, 1080)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Lessons_Select)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(Lessons_Select)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/background/figs/background/规范.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.base_frame = QtWidgets.QFrame(Lessons_Select)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.base_frame.sizePolicy().hasHeightForWidth())
        self.base_frame.setSizePolicy(sizePolicy)
        self.base_frame.setStyleSheet("QFrame{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,stop:0 rgb(0, 170, 255), stop:1 rgba(0, 0, 0, 255));}")
        self.base_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.base_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.base_frame.setObjectName("base_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.base_frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.left_fig = QtWidgets.QVBoxLayout()
        self.left_fig.setObjectName("left_fig")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.left_fig.addItem(spacerItem1)
        self.lab_left_fig = QtWidgets.QLabel(self.base_frame)
        self.lab_left_fig.setMinimumSize(QtCore.QSize(150, 150))
        self.lab_left_fig.setMaximumSize(QtCore.QSize(150, 150))
        self.lab_left_fig.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 8px;")
        self.lab_left_fig.setText("")
        self.lab_left_fig.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_left_fig.setObjectName("lab_left_fig")
        self.left_fig.addWidget(self.lab_left_fig)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.left_fig.addItem(spacerItem2)
        self.lab_left_title = QtWidgets.QLabel(self.base_frame)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lab_left_title.setFont(font)
        self.lab_left_title.setStyleSheet("color:rgb(255, 255, 255);background-color:rgba(255, 255, 255, 0)")
        self.lab_left_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_left_title.setObjectName("lab_left_title")
        self.left_fig.addWidget(self.lab_left_title)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.left_fig.addItem(spacerItem3)
        self.horizontalLayout_2.addLayout(self.left_fig)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.lab_center_fig = QtWidgets.QLabel(self.base_frame)
        self.lab_center_fig.setMinimumSize(QtCore.QSize(250, 250))
        self.lab_center_fig.setMaximumSize(QtCore.QSize(250, 250))
        self.lab_center_fig.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"")
        self.lab_center_fig.setText("")
        self.lab_center_fig.setObjectName("lab_center_fig")
        self.verticalLayout.addWidget(self.lab_center_fig)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)
        self.lab_center_title = QtWidgets.QLabel(self.base_frame)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lab_center_title.setFont(font)
        self.lab_center_title.setStyleSheet("color:rgb(255, 255, 255);background-color:rgba(255, 255, 255, 0)")
        self.lab_center_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_center_title.setObjectName("lab_center_title")
        self.verticalLayout.addWidget(self.lab_center_title)
        spacerItem7 = QtWidgets.QSpacerItem(247, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem7)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 2)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem8)
        self.right_fig = QtWidgets.QVBoxLayout()
        self.right_fig.setObjectName("right_fig")
        spacerItem9 = QtWidgets.QSpacerItem(20, 264, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.right_fig.addItem(spacerItem9)
        self.lab_right_fig = QtWidgets.QLabel(self.base_frame)
        self.lab_right_fig.setMinimumSize(QtCore.QSize(150, 150))
        self.lab_right_fig.setMaximumSize(QtCore.QSize(150, 150))
        self.lab_right_fig.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 8px;")
        self.lab_right_fig.setText("")
        self.lab_right_fig.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_right_fig.setObjectName("lab_right_fig")
        self.right_fig.addWidget(self.lab_right_fig)
        spacerItem10 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.right_fig.addItem(spacerItem10)
        self.lab_right_title = QtWidgets.QLabel(self.base_frame)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lab_right_title.setFont(font)
        self.lab_right_title.setStyleSheet("color:rgb(255, 255, 255);background-color:rgba(255, 255, 255, 0)")
        self.lab_right_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_right_title.setObjectName("lab_right_title")
        self.right_fig.addWidget(self.lab_right_title)
        spacerItem11 = QtWidgets.QSpacerItem(20, 263, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.right_fig.addItem(spacerItem11)
        self.horizontalLayout_2.addLayout(self.right_fig)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem12)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.bottom = QtWidgets.QVBoxLayout()
        self.bottom.setObjectName("bottom")
        self.table = QtWidgets.QHBoxLayout()
        self.table.setObjectName("table")
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.table.addItem(spacerItem13)
        self.lab_describe = QtWidgets.QLabel(self.base_frame)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.lab_describe.setFont(font)
        self.lab_describe.setStyleSheet("color:rgb(255, 255, 255);background-color:rgba(255, 255, 255, 0)")
        self.lab_describe.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_describe.setObjectName("lab_describe")
        self.table.addWidget(self.lab_describe)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.table.addItem(spacerItem14)
        self.table.setStretch(0, 1)
        self.table.setStretch(2, 1)
        self.bottom.addLayout(self.table)
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.bottom.addItem(spacerItem15)
        self.select_btn = QtWidgets.QHBoxLayout()
        self.select_btn.setObjectName("select_btn")
        self.btn_left = QtWidgets.QPushButton(self.base_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_left.sizePolicy().hasHeightForWidth())
        self.btn_left.setSizePolicy(sizePolicy)
        self.btn_left.setMinimumSize(QtCore.QSize(200, 50))
        self.btn_left.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.btn_left.setFont(font)
        self.btn_left.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.btn_left.setStyleSheet("color: rgb(255, 255, 255);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/figs/icon/左箭头.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_left.setIcon(icon)
        self.btn_left.setIconSize(QtCore.QSize(50, 50))
        self.btn_left.setFlat(True)
        self.btn_left.setObjectName("btn_left")
        self.select_btn.addWidget(self.btn_left)
        self.btn_enter = QtWidgets.QPushButton(self.base_frame)
        self.btn_enter.setMinimumSize(QtCore.QSize(100, 60))
        self.btn_enter.setMaximumSize(QtCore.QSize(100, 60))
        self.btn_enter.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/figs/icon/登入.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_enter.setIcon(icon1)
        self.btn_enter.setIconSize(QtCore.QSize(55, 55))
        self.btn_enter.setFlat(True)
        self.btn_enter.setObjectName("btn_enter")
        self.select_btn.addWidget(self.btn_enter)
        self.btn_right = QtWidgets.QPushButton(self.base_frame)
        self.btn_right.setMinimumSize(QtCore.QSize(200, 50))
        self.btn_right.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.btn_right.setFont(font)
        self.btn_right.setStyleSheet("color: rgb(255, 255, 255);")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/figs/icon/右箭头.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_right.setIcon(icon2)
        self.btn_right.setIconSize(QtCore.QSize(50, 50))
        self.btn_right.setFlat(True)
        self.btn_right.setObjectName("btn_right")
        self.select_btn.addWidget(self.btn_right)
        self.bottom.addLayout(self.select_btn)
        self.back_layout = QtWidgets.QHBoxLayout()
        self.back_layout.setObjectName("back_layout")
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.back_layout.addItem(spacerItem16)
        self.btn_back = QtWidgets.QPushButton(self.base_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_back.sizePolicy().hasHeightForWidth())
        self.btn_back.setSizePolicy(sizePolicy)
        self.btn_back.setMinimumSize(QtCore.QSize(200, 50))
        self.btn_back.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.btn_back.setFont(font)
        self.btn_back.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btn_back.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_back.setStyleSheet("QPushButton{color: rgb(255, 255, 255);border:none}\n"
"QPushButton:hover{padding-bottom:8px}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/figs/icon/返回.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_back.setIcon(icon3)
        self.btn_back.setIconSize(QtCore.QSize(50, 50))
        self.btn_back.setObjectName("btn_back")
        self.back_layout.addWidget(self.btn_back)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.back_layout.addItem(spacerItem17)
        self.bottom.addLayout(self.back_layout)
        self.verticalLayout_2.addLayout(self.bottom)
        self.verticalLayout_3.addWidget(self.base_frame)
        self.base_frame.raise_()
        self.label.raise_()

        self.retranslateUi(Lessons_Select)
        QtCore.QMetaObject.connectSlotsByName(Lessons_Select)

    def retranslateUi(self, Lessons_Select):
        _translate = QtCore.QCoreApplication.translate
        Lessons_Select.setWindowTitle(_translate("Lessons_Select", "Form"))
        self.lab_left_title.setText(_translate("Lessons_Select", "TextLabel"))
        self.lab_center_title.setText(_translate("Lessons_Select", "TextLabel"))
        self.lab_right_title.setText(_translate("Lessons_Select", "TextLabel"))
        self.lab_describe.setText(_translate("Lessons_Select", "lab_describe"))
        self.btn_left.setText(_translate("Lessons_Select", "上一个"))
        self.btn_right.setText(_translate("Lessons_Select", "下一个"))
        self.btn_back.setText(_translate("Lessons_Select", "返回上一级"))
import res_rc