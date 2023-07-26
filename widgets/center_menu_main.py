import sys,os, cv2

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
# path = os.path.dirname(__file__)
# path = "/".join(path.split("\\")[:-1])
# sys.path.append(path)

from .ui import Ui_Center_Menu
from .lessons_select_main import Lessons_Select_Main
from .setting_main import Setting_Main
from .Grade_main import Grade_std, Grade_reaction

class Center_Menu_Main(QWidget,Ui_Center_Menu):

    def __init__(self, db, student_id, is_Standard):
        super(Center_Menu_Main, self).__init__()

        self.db = db
        self.student_id = student_id
        self.is_Standard = is_Standard
        self.setupUi(self)
        self.windowinit()
        if not self.is_Standard:
            self.changeUi()
        self.initfun()
    
    def windowinit(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def changeUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.btn_nextWindow.setText(_translate("Center_Menu", "动作反应训练课程选择"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/figs/icon/对抗训练.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_nextWindow.setIcon(icon)

    def initfun(self):
        self.btn_back.clicked.connect(self.close)
        self.btn_nextWindow.clicked.connect(self.open_LessonWindow)
        self.btn_grade.clicked.connect(self.open_GradeWindow)

    def open_SettingWindow(self):
        self.nextWindow = Setting_Main(self)
        self.nextWindow.show()
        self.hide()
    def open_GradeWindow(self):
        if self.is_Standard:
            self.nextWindow = Grade_std(self, self.db, self.student_id)
        else:
            self.nextWindow = Grade_reaction(self, self.db, self.student_id)
        self.nextWindow.show()
        self.hide
    def open_LessonWindow(self):
        if self.is_Standard:
            self.nextWindow = Lessons_Select_Main(self, self.db, self.student_id, is_Standard=True)
        else:
            self.nextWindow = Lessons_Select_Main(self, self.db, self.student_id)

        self.nextWindow.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Center_Menu_Main()
    win.show()
    sys.exit(app.exec_())