import sys 
import time 
import datetime 
import json
import requests
import os
import numpy as np
from multiprocessing import Event, Queue, Process

from PyQt5.QtWidgets import QApplication,QWidget,QGraphicsOpacityEffect,QMessageBox
from PyQt5 import QtCore, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from auxiliary_tools import skeleton_get, parse_data, draw_skeleton2d,\
    action_evaluation, skeleton_from_video, skeleton_trans_ntu
from auxiliary_tools.count_main import count
from .Std_show_main import Std_show
from .ui import Ui_Action_FollowP1


class Action_Eval_Main(QWidget,Ui_Action_FollowP1):
    def __init__(self, parent, db, action_id, student_id):
        super(Action_Eval_Main, self).__init__()
        self.parent = parent
        self.db = db
        self.action_id = action_id
        self.student_id = student_id
        self.setupUi(self)
        self.windowinit()
        
        self.load_config()
        self.start_process()
        self.getActionInfo()
        self.initfun()
    
    def windowinit(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def load_config(self, json_path='./data/sensor/config.json'):
        # 获取有关传感器和摄像头的信息
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
        # 初始化各定时器和倒计时时长，各定时器和对应的处理函数绑定
        # 倒计时定时器，时间戳定时器，姿态估计结果收集定时器
        self.num = 5
        self.tip_timer = QtCore.QTimer()
        self.tip_timer.timeout.connect(self.change_num)
        self.timer_stamp = QtCore.QTimer()
        self.timer_stamp.timeout.connect(self.timecheck)
        self.timer_collect = QtCore.QTimer()
        self.timer_collect.timeout.connect(self.collect_skeleton)
        self.tip_timer.start(1000)

    def get_ip(self):
        # 获取课程视频服务端的信息，ip以及端口
        json_path = "./data/dbconfig/database_account_password.json"
        with open(json_path) as f:
            data_base_json = json.load(f)        
        return data_base_json["video_ip"], data_base_json["course_dir"]

    def requestvideo(self):
        self.video_ip, self.course_dir = self.get_ip()
        course_url = "http://" + self.video_ip + self.course_dir + self.course_path
        response = requests.get(course_url)
        self.course_path = './data/course_action/std/' + os.path.basename(self.course_path)
        
        if not os.path.exists(os.path.dirname(self.course_path)):
            os.makedirs(os.path.dirname(self.course_path))
        if not os.path.exists(self.course_path):
            with open(self.course_path, 'wb') as f:
                f.write(response.content)
        
        skeleton_url = "http://" + self.video_ip + self.course_dir + self.skeleton_path
        
        npy_path = os.path.splitext(self.course_path)[0] + '.npy'

        response2 = requests.get(skeleton_url)
        if(response2.status_code != 404):
            with open(npy_path, 'wb') as f:
                f.write(response2.content)



    def getActionInfo(self):
        # 获取课程视频，存储在本地
        sql_course = """SELECT action_Path, action_Name, course_ID, skeleton_path
                    FROM action_info
                    WHERE action_ID = {}""".format(self.action_id)
        course_info = self.db.search_table(sql_course)
        
        self.course_path = course_info[0][0]
        self.course_Name = course_info[0][1]
        
        self.course_id = course_info[0][2]
        self.skeleton_path = course_info[0][3]
        self.requestvideo()

       
        # self.action_path = r'E:\PoseUI\PoseUI\data\camera_video_demo\camera_192.168.1.2.mp4'
        # self.action_Length = 1500
        # self.action_Name = ",adad"
        # self.action_path = r'C:\Users\user\Desktop\新建文件夹\test_video\A03N042.mp4'
    
    def ready(self):
        # 初始化视频播放控件，开启播放过程中需要的两个定时器
        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(self.videoWidget)
        media = QtCore.QUrl.fromLocalFile(self.course_path)
        self.player.setMedia(QMediaContent(media))
        self.player.play()        
        self.timer_stamp.start(30)
        self.timequeue.put((0, 0))
        self.S_skeleton = []
        self.timer_collect.start(1)
        self.start_time = time.time()

    def change_num(self):
        if self.stop_event.is_set():
            self.tip_timer.stop()
            if self.parent != None:
                self.parent.show()
            QMessageBox.warning(self, "警告","请检查传感器连接", QMessageBox.Yes)
            for i in self.process_id:
                i.join()
            self.close()
        # 倒计时，每秒触发一次
        opacity = QGraphicsOpacityEffect()
        self.lab_tip.setStyleSheet("color: rgb(255, 255, 255);\n"
                                     "background-color: rgb(0, 0, 0);\n"
                                     "font: 100pt \"Pristina\";")
        if self.num > 0:
            for i in range(self.num*10, self.num*10 - 10, -1):
                self.lab_tip.setText(str(self.num))
                self.lab_tip.repaint()
                opacity.setOpacity((i + 10) / 50)
                self.lab_tip.setGraphicsEffect(opacity)
                time.sleep(0.05)
            self.num -= 1
        elif self.num == 0:
            self.lab_tip.setText("开始！")
            self.lab_tip.repaint()
            self.num -=1
        else:
            self.lab_tip.hide()
            self.tip_timer.stop()
            self.ready()

    def timecheck(self):
        # 控制摄像头采集
        current_time = time.time()
        # 判断视频是否播放完
        if((current_time - self.start_time)*1000 >  500 + self.player.duration()):
            if self.timequeue.qsize() == 0 and self.corqueue.qsize() == 0:
                self.timequeue.put((current_time, 1))           
                self.start_judge()
                self.timer_stamp.stop()
            else:
                return
        self.timequeue.put((current_time, 0))

    def collect_skeleton(self):
        # 收集汇总姿态估计结果
        if self.corqueue.qsize():
            _, skeleton, _ = self.corqueue.get()
            self.S_skeleton.append(skeleton_trans_ntu(skeleton))

    def start_process(self):
        # 运行各个子进程
        # 使用传感器获取姿态数据需要接受传感器信息的start_server进程
        # 解析数据的parse_data进程，展示学员骨架的draw_skeleton2d进程
        # 基于摄像头获取姿态数据只需要skeleton_get进程(画图展示包含在其中)
        self.stop_event = Event()
        self.timequeue = Queue(10)
        self.corqueue = Queue(10)
        self.drawqueue = Queue(10)
        self.process_id = []
        self.count_queue = None
        self.count_re = None
        # 传感器模式下无法实现计数
        if self.using_sensor:
            self.process_id.append(Process(target=parse_data,
                                      args=(self.stop_event,
                                            self.timequeue, 
                                            self.corqueue, 
                                            self.drawqueue)))
            self.process_id.append(Process(target=draw_skeleton2d, 
                                      args=(self.stop_event, 
                                            self.drawqueue)))
        else:
            sql_count = """select count_flag 
                    from action_info 
                    where action_ID = {}""".format(self.action_id)
            self.count_flag = self.db.search_table(sql_count)[0][0] == 1
            if self.count_flag:
                self.count_queue = Queue(10)
                self.count_re = Queue(1)
                # self.process_id.append(Process(target=count,
                #                     args=(self.stop_event, 
                #                             self.count_queue, 
                #                             self.count_re)))
            self.process_id.append(Process(target=skeleton_get, 
                                      args=(self.stop_event,  
                                            self.timequeue, 
                                            self.corqueue,
                                            None, 
                                            None, 
                                            self.camera, False)))


        temp = Process(target=count,
                        args=(self.stop_event, 
                        self.count_queue, 
                        self.count_re))
        temp.start()
        for i in self.process_id:
            # i.daemon = True
            i.start()

    def start_judge(self):
        # 动作比对和结果展示

        self.timer_collect.stop()
        npy_path = os.path.splitext(self.course_path)[0] + '.npy'
        if os.path.exists(npy_path):
            T_skeleton = np.load(npy_path)
        else:
            T_skeleton = skeleton_from_video(self.course_path)
            np.save(npy_path, T_skeleton)
        score, grade, disp_T, disp_S, error_part = action_evaluation(T_skeleton, self.S_skeleton)
        if self.count_flag:
            while(self.count_re.empty()):
                continue
            count = self.count_re.get()
        self.score = grade
        self.timequeue.put((0,2))
        if(len(disp_S) == 0):
            disp_S = [0]
            disp_T = [0]
        T_sk = [T_skeleton[i] for i in disp_T]
        S_sk = [self.S_skeleton[i] for i in disp_S]
        self.grade_window = Std_show(self, S_sk, T_sk, grade, error_part)
        self.grade_window.show()
        self.hide()
    def upload(self):
        # 成绩上传
        sql_upload = """INSERT grade_std 
                            (student_ID, course_ID, action_ID, grade, train_time)
                            VALUES(%s, %s, %s, %s, %s)
                            """
        t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        args = [[self.student_id, self.course_id, self.action_id, self.score, t]]
        self.db.insert_data(sql=sql_upload, args=args)

    def back(self):
        self.stop_event.set()
        self.player.stop()
        time.sleep(0.5)
        if self.parent != None:
            self.parent.show()
        self.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Action_Eval_Main()
    win.show()
    sys.exit(app.exec_())