import sys
import numpy as np
import cv2
# import face_recognition, cv2


from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5 import QtGui, QtCore

from auxiliary_tools import DatabaseOperation
from .ui import Ui_Login
from .center_menu_main import Center_Menu_Main


class LogMain(QMainWindow, Ui_Login):
    face_signal = pyqtSignal()
    def __init__(self):
        super(LogMain, self).__init__()        
        self.setupUi(self)
        self.windowinit()
        self.initfun()
        
    def initfun(self):
        #按钮点击和槽函数绑定
        self.btn_close.clicked.connect(self.close)
        self.btn_open.clicked.connect(self.change_CameraState)
        # self.btn_open.clicked.connect(self.open_SelectWindow)

        #触发摄像头画面显示函数的定时器
        self.timer_camera = QtCore.QTimer()
        self.timer_camera.timeout.connect(self.show_camera)
        
        #跳转到选择功能界面,将下一界面的前置界面设置为当前界面
        #人脸识别成功信号和处理函数链接
        self.face_signal.connect(self.open_SelectWindow)
              
        #摄像头
        self.cap = cv2.VideoCapture()
        
        #获取学员信息
        self.db = DatabaseOperation()
        self.get_StuInfo()
        self.currentname = 'Unknown'
        self.face_count = 0
        self.error_count = 0
        self.show_img = None
        self.student_id = 7
    
    def windowinit(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.back1.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
    
    def open_SelectWindow(self):
        #关闭定时器，释放相机，改变按钮文本，隐藏当前界面，打开下一界面
        print(self.currentname)
        self.select_Window = Center_Menu_Main(self, self.db, self.student_id)
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
            # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
            # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
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
            self.lab_camera.setPixmap(QtGui.QPixmap(":/icons/figs/icon/user110.png"))

    def show_camera(self):
        #获取视频中的人脸位置和每张人脸的特征
        flag, image = self.cap.read()
        # if not flag:
        #     return
        # image = image[340:740, 660:1260]
        image = cv2.resize(image, (640,360))
        image = cv2.flip(image, 1)
        image = image[130:230, 270:370]
        self.show_img = cv2.resize(image, (100, 100))
        self.show_img = cv2.cvtColor(self.show_img, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(self.show_img.data, self.show_img.shape[1], self.show_img.shape[0], self.show_img.shape[1] * 3,QtGui.QImage.Format_RGB888)
        self.lab_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

        face_locations = face_recognition.face_locations(image)

        face_encodings = face_recognition.face_encodings(image, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            line_corlor = (0,255,0)
            line_thickness = 1
            hir = 6
            ver = 20
            image = cv2.line(image, [left, top],[right, top], line_corlor, line_thickness)
            image = cv2.line(image, [right, top],[right, bottom], line_corlor, line_thickness)
            image = cv2.line(image, [right, bottom],[left, bottom], line_corlor, line_thickness)
            image = cv2.line(image, [left, bottom],[left, top], line_corlor, line_thickness)
            #显示当前画面
            self.show_img = cv2.resize(image, (100, 100))
            self.show_img = cv2.cvtColor(self.show_img, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(self.show_img.data, self.show_img.shape[1], self.show_img.shape[0], self.show_img.shape[1] * 3,QtGui.QImage.Format_RGB888)
            self.lab_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
            name = 'Unknown'
            match = face_recognition.compare_faces(self.feature, face_encoding, tolerance=0.4)
            if True in match:
                #获取当前人脸的名字
                i = match.index(True)
                name = self.name[i]
            if name == 'Unknown':
                #未知人员
                self.error_count += 1
                break
            elif name == self.currentname:
                #与当前人脸一致
                self.face_count += 1
                self.error_count = 0
                break
            else:
                #与当前人脸不一致
                self.face_count = 0
                self.error_count += 1
                self.currentname = name
                break
            
        if self.face_count > 5:
            #登录成功
            self.student_id = self.get_student_id(name)
            self.face_signal.emit()
            self.face_count = 0
            self.currentname = 'Unknown'
            self.select_Window.user_name = name
            self.select_Window.user_ProfilePhoto = self.img[i]
        

            # image = image[top-40:bottom+30,left-6:right+6]
            

        if self.error_count > 10:
            #登录失败
            self.change_CameraState()
            self.error_count = 0
            self.face_count = 0
            self.currentname = 'Unknown'
            self.back2.setText("登录失败")

    def get_student_id(self, name):
        sql_student = """   SELECT user_id
                            FROM student_info
                            WHERE username='{}'""".format(name)
        data = self.db.search_table(sql_student)
        return data[0][0]
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = LogMain()
    mainWindow.show()
    sys.exit(app.exec_())