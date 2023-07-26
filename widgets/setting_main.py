import numpy as np
import cv2
from PyQt5 import QtCore, QtWidgets
import json
from PyQt5.QtWidgets import QWidget

from .ui import Ui_Setting_Widget
from auxiliary_tools.processtest import load_json
class Setting_Main(QWidget, Ui_Setting_Widget):
    def __init__(self, parent):
        super(Setting_Main, self).__init__()
        self.setupUi(self)
        self.windowinit()
        
        self.parent = parent
        self.initfun()
    
    def windowinit(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    
    def initfun(self):
        self.btn_save.clicked.connect(self.save_all)
        self.btn_exit.clicked.connect(self.exit)
        self.config = load_json('./data/sensor/config.json')
        self.lineEdit.setText(str(self.config["camera"]))
        if self.config["using_sensor"] == 'F':
            self.btn_sensor.setChecked(False)
            self.btn_camera.setChecked(True)
        else:
            self.btn_sensor.setChecked(True)
            self.btn_camera.setChecked(False)

    def save_all(self):
        self.config["camera"] = self.lineEdit.text()
        
        if self.btn_sensor.isChecked():
            self.config["using_sensor"] = 'T'
        else:
            self.config["using_sensor"] = 'F'
            cap = cv2.VideoCapture(self.config["camera"])
            flag, _ = cap.read()
            if not flag:
                QtWidgets.QMessageBox.warning(self, u"Warning", u"相机名称有误",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
                cap.release()
                return
        with open('./data/sensor/config.json','r') as f:
            json.dump(self.config, f)

    def exit(self):
        self.parent.show()
        self.close()
