import sys

import cv2
import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget

from .action_select_main import Action_Select_Main
from .reaction_train_main import Reaction_Train_Main
from .ui import Ui_Lessons_Select


class Lessons_Select_Main(QWidget, Ui_Lessons_Select):

    def __init__(self, parent, db, student_id, is_Standard=False):
        super(Lessons_Select_Main, self).__init__()
        self.setupUi(self)
        self.windowinit()

        self.parent = parent
        self.db = db
        self.student_id = student_id

        self.getCourseInfo(is_Standard)
        self.initfun(is_Standard)
        if not is_Standard:
            self.label.setPixmap(QtGui.QPixmap(":/background/figs/background/反应.png"))


    def windowinit(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def getCourseInfo(self, is_Standard):
        if is_Standard:
            sql_course = """SELECT course_ID,course_Name,course_Icon,course_Description
                            FROM course_standard
                            WHERE del_flag!=1"""
        else:
            sql_course = """SELECT course_ID,course_Name,course_Icon,course_Description
                            FROM course_actionresponse
                            WHERE del_flag!=1"""
        data = self.db.search_table(sql_course)
        self.course_ID = [data[i][0] for i in range(len(data))]
        self.course_Name = [data[i][1] for i in range(len(data))]
        self.course_Icon = [data[i][2] for i in range(len(data))]
        for i in range(len(self.course_Icon)):
            img = cv2.imdecode(np.frombuffer(
                self.course_Icon[i], np.uint8), cv2.IMREAD_COLOR)
            self.course_Icon[i] = img
        self.course_Description = [data[i][3] for i in range(len(data))]
        self.index = 0

    def initfun(self, is_Standard):
        self.btn_back.clicked.connect(self.back)
        self.btn_left.clicked.connect(self.changeCourse)
        self.btn_right.clicked.connect(self.changeCourse)
        if is_Standard:
            self.btn_enter.clicked.connect(self.enterLesson_standard)
        else:
            self.btn_enter.clicked.connect(self.enterLesson_reaction)
        self.showcourse()

    def showcourse(self):
        # 根据课程index展示课程
        self.lab_describe.setText(self.course_Description[self.index])
        self.lab_center_title.setText(self.course_Name[self.index])
        self.lab_left_title.setText(
            self.course_Name[(self.index-1) % len(self.course_ID)])
        self.lab_right_title.setText(
            self.course_Name[(self.index+1) % len(self.course_ID)])

        # 当前课程
        img = cv2.resize(self.course_Icon[self.index], (250, 250))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(
            img.data, img.shape[0], img.shape[1], img.shape[1] * 3, QtGui.QImage.Format_RGB888)
        self.lab_center_fig.setPixmap(QtGui.QPixmap.fromImage(img))

        # 前一课程
        img = cv2.resize(
            self.course_Icon[(self.index-1) % len(self.course_ID)], (150, 150))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(
            img.data, img.shape[0], img.shape[1], img.shape[1] * 3, QtGui.QImage.Format_RGB888)
        self.lab_left_fig.setPixmap(QtGui.QPixmap.fromImage(img))

        # 后一课程
        img = cv2.resize(
            self.course_Icon[(self.index+1) % len(self.course_ID)], (150, 150))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(
            img.data, img.shape[0], img.shape[1], img.shape[1] * 3, QtGui.QImage.Format_RGB888)
        self.lab_right_fig.setPixmap(QtGui.QPixmap.fromImage(img))

    def enterLesson_reaction(self):
        # 进入动作反应训练界面
        self.next_window = Reaction_Train_Main(
            self, self.db, self.course_ID[self.index], self.student_id)
        self.next_window.show()
        self.hide()

    def enterLesson_standard(self):
        # 进入动作选择界面
        self.next_window = Action_Select_Main(
            self, self.db, self.course_ID[self.index], self.student_id)
        self.next_window.show()
        self.hide()

    def changeCourse(self):
        if self.sender().objectName() == 'btn_left':
            self.index -= 1
        else:
            self.index += 1
        self.index = (self.index + len(self.course_ID)) % len(self.course_ID)
        self.showcourse()

    def back(self):
        # 回到控制中心界面
        self.close()
        self.parent.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Lessons_Select_Main()
    win.show()
    sys.exit(app.exec_())
