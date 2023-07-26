import json
import os
import sys
import time
import requests
import datetime
from multiprocessing import Event, Process, Queue
from PyQt5.QtWidgets import QApplication,QWidget, QGraphicsOpacityEffect
from PyQt5 import  QtCore, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from followtest import Ui_Form

class followtest_Main(QWidget, Ui_Form):
    def __init__(self, parent, db, course_id, student_id):
        super(followtest_Main, self).__init__()
        self.parent = parent
        self.db = db
        self.course_id = course_id
        self.student_id = student_id      
        self.setupUi(self)
        self.windowinit()

        self.load_config()
        self.start_process()
        self.getCourseInfo()
        self.initfun() 

    def windowinit(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        # self.player_frame.setMouseTracking(True)
        self.videoWidget.setMouseTracking(True)

    def load_config(self, json_path='./data/sensor/config.json'):
        with open(json_path, encoding='UTF-8') as f:
            config = json.load(f)
        if config["using_sensor"] == 'F':
            self.using_sensor = False
        else:
            self.using_sensor = True
        if len(config["camera"]) == 1:
            self.camera = int(config["camera"])
        else:
            self.camera = config["camera"]
    
    def initfun(self):
        self.btn_exchange.clicked.connect(self.exchange)
    def exchange(self,evnet):
        print('hhh')
    
    def getCourseInfo(self):
        pass
    def start_process(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = followtest_Main(0,0,0,0)
    window.show()
    sys.exit(app.exec_())