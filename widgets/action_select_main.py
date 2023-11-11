import sys, cv2
import numpy as np

from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5 import QtCore, QtGui


from .ui import Ui_Lessons_Select
from .std_train_select_main import Std_Train_Select_Main


class Action_Select_Main(QWidget,Ui_Lessons_Select):

    def __init__(self, parent, db, course_id, student_id):
        super(Action_Select_Main, self).__init__()
        self.setupUi(self)
        self.windowinit()

        self.parent = parent
        self.db = db
        self.course_id = course_id
        self.student_id = student_id
        self.initfun()
        self.getCourseInfo()
        self.showcourse()

    def windowinit(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def getCourseInfo(self):
        sql_course = """SELECT action_ID, action_Name, action_Icon, action_Description
                        FROM action_info
                        WHERE course_id={} AND del_flag!=1""".format(self.course_id)
        data = self.db.search_table(sql_course)
        self.action_ID = [data[i][0] for i in range(len(data))]
        self.course_Name = [data[i][1] for i in range(len(data))]
        self.course_Icon = [data[i][2] for i in range(len(data))]
        for i in range(len(self.course_Icon)):
            img = cv2.imdecode(np.frombuffer(self.course_Icon[i], np.uint8), cv2.IMREAD_COLOR)
            self.course_Icon[i] = img
        self.course_Description = [data[i][3] for i in range(len(data))]
        self.index = 0

    def initfun(self):
        self.btn_back.clicked.connect(self.back)
        self.btn_left.clicked.connect(self.changeCourse)
        self.btn_right.clicked.connect(self.changeCourse)
        self.btn_enter.clicked.connect(self.enterStdTrain)
        

    def showcourse(self):
        # 根据课程index展示课程
        self.lab_describe.setText(self.course_Description[self.index])
        self.lab_center_title.setText(self.course_Name[self.index])
        self.lab_left_title.setText(
            self.course_Name[(self.index-1) % len(self.action_ID)])
        self.lab_right_title.setText(
            self.course_Name[(self.index+1) % len(self.action_ID)])

        #当前课程
        img = cv2.resize(self.course_Icon[self.index], (250, 250))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(
            img.data, img.shape[0], img.shape[1], img.shape[1] * 3, QtGui.QImage.Format_RGB888)
        self.lab_center_fig.setPixmap(QtGui.QPixmap.fromImage(img))

        #前一课程
        img = cv2.resize(
            self.course_Icon[(self.index-1) % len(self.action_ID)], (150, 150))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(
            img.data, img.shape[0], img.shape[1], img.shape[1] * 3, QtGui.QImage.Format_RGB888)
        self.lab_left_fig.setPixmap(QtGui.QPixmap.fromImage(img))

        #后一课程
        img = cv2.resize(
            self.course_Icon[(self.index+1) % len(self.action_ID)], (150, 150))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(
            img.data, img.shape[0], img.shape[1], img.shape[1] * 3, QtGui.QImage.Format_RGB888)
        self.lab_right_fig.setPixmap(QtGui.QPixmap.fromImage(img))

    def enterStdTrain(self):
        # 进入动作反应训练界面
        self.next_window = Std_Train_Select_Main(self, self.db, self.action_ID[self.index], self.student_id)

        self.next_window.show()
        self.hide()
   
    def changeCourse(self):
        if self.sender().objectName() == 'btn_left':
            self.index -= 1
        else:
            self.index += 1
        self.index = (self.index + len(self.action_ID)) % len(self.action_ID)
        self.showcourse()

    def back(self):
        #回到控制中心界面
        self.close()
        self.parent.show()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Action_Select_Main()
    win.show()
    sys.exit(app.exec_())