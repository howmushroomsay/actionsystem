import sys
import cv2
import face_recognition
import os
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QWidget

from auxiliary_tools import DatabaseOperation

from .center_menu_main import Center_Menu_Main
from .ui import Ui_Login, Ui_Login_Background


class Login_Background_Main(QWidget,Ui_Login_Background):

    def __init__(self):
        super(Login_Background_Main, self).__init__()
        self.setupUi(self)
        self.windowinit()
        import os.path as osp

        self.movie = QMovie("./widgets/figs/other_resources/log_background.gif")
        self.movie.setSpeed(80)
        self.label.setMovie(self.movie)
        self.movie.start()


    def windowinit(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)


class Login_Main(QWidget,Ui_Login):
    face_signal = pyqtSignal()
    def __init__(self):
        super(Login_Main, self).__init__()
        self.setupUi(self)
        self.windowinit()
        self.background = Login_Background_Main()
        self.background.show()

        self.initfun()

    def windowinit(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    
    
    def initfun(self):
        #按钮点击和槽函数绑定
        self.btn_open.clicked.connect(self.change_CameraState)
        # self.btn_open.clicked.connect(self.open_SelectWindow)
        self.btn_close.clicked.connect(self.all_close)
        
        #触发摄像头画面显示函数的定时器
        self.timer_camera = QtCore.QTimer()
        self.timer_camera.timeout.connect(self.show_camera)
        
        #跳转到选择功能界面,将下一界面的前置界面设置为当前界面
        #人脸识别成功信号和处理函数链接
        self.face_signal.connect(self.open_SelectWindow)
        
        #摄像头
        self.cap = cv2.VideoCapture()
        
        #获取学员信息
        # self.db = 0
        self.db = DatabaseOperation()
        self.get_StuInfo()
        self.currentname = 'Unknown'
        self.face_count = 0
        self.error_count = 0

        

    def open_SelectWindow(self):
        #关闭定时器，释放相机，改变按钮文本，隐藏当前界面，打开下一界面
        print(self.currentname)
        self.select_Window = Center_Menu_Main(self, self.db)
        self.timer_camera.stop()        
        self.cap.release()
        self.btn_open.setText("打开相机")
        self.hide()
        self.select_Window.show()

    def get_StuInfo(self):
        #获取学员信息，包括登录账号和密码，人脸，人脸特征
        sql_student = """   SELECT username, face_data, face_encoding
                            FROM student_info"""
        data = self.db.search_table(sql_student)
        self.name = [i[0] for i in data]
        self.img  = [i[1] for i in data]
        self.feature = [i[2] for i in data]
        for i in range(len(self.img)):
            self.img[i] = cv2.imdecode(np.frombuffer(self.img[i], np.uint8), cv2.IMREAD_COLOR)
        for i in range(len(self.feature)):
            self.feature[i] = np.frombuffer(self.feature[i], dtype=np.float64)

    def change_CameraState(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(0)
            if not flag:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                #开启定时器，定时获取摄像头画面
                self.timer_camera.start(25)
                self.btn_open.setText("关闭相机")
        else:
            #关闭定时器，不再获取摄像头画面，并将人脸识别置于初始状态
            self.timer_camera.stop()
            self.cap.release()
            self.currentname = 'Unknown'
            self.face_count = 0
            self.error_count = 0
            self.btn_open.setText("打开相机")
            self.lab_camera.setPixmap(QtGui.QPixmap(":/icons/figs/icon/log_user.png"))

    def show_camera(self):
        #获取视频中的人脸位置和每张人脸的特征
        flag, image = self.cap.read()
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = 'Unknown'
            match = face_recognition.compare_faces(self.feature, face_encoding, tolerance=0.3)
            if True in match:
                #获取当前人脸的名字
                i = match.index(True)
                name = self.name[i]
            if name == 'Unknown':
                #未知人员
                self.error_count += 1
            elif name == self.currentname:
                #与当前人脸一致
                self.face_count += 1
                self.error_count = 0
            else:
                #与当前人脸不一致
                self.face_count = 0
                self.error_count += 1
                self.currentname = name
            
            if self.face_count > 3:
                #登录成功
                self.face_signal.emit()
                self.face_count = 0
                self.currentname = 'Unknown'
                self.select_Window.user_name = name
                self.select_Window.user_ProfilePhoto = self.img[i]

            image = image[top-40:bottom+30,left-6:right+6]
        try:
            #显示当前画面
            show = cv2.resize(image, (200, 200))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], show.shape[1] * 3,QtGui.QImage.Format_RGB888)
            self.lab_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        except:
            pass
        if self.error_count > 10:
            #登录失败
            self.change_CameraState()
            self.error_count = 0
            self.face_count = 0
            self.currentname = 'Unknown'
            self.text_welcome.setText("登录失败")
    def all_close(self):
        self.background.close()
        self.close()


if __name__ == "__main__":
    '''
    本界面测试需要修改gif资源路径
    '''
    app = QApplication(sys.argv)
    mainWindow = Login_Main()
    mainWindow.show()
    sys.exit(app.exec_())