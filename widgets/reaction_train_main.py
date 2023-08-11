import json
import os
import requests
import datetime
from multiprocessing import Event, Process, Queue
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt5 import  QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from .ui import Ui_Form

from auxiliary_tools import skeleton_get, seg, actionRec, parse_data
from .reaction_train_contral import Reaction_Result, Reaction_Train_Player_Frame

class Reaction_Train_Main(QWidget, Ui_Form):
    def __init__(self, parent, db, course_id, student_id):
        super(Reaction_Train_Main, self).__init__()
        self.parent = parent
        self.db = db
        self.course_id = course_id
        self.student_id = student_id      
        self.setupUi(self)
        self.windowinit()

        self.hint_frame = Reaction_Train_Player_Frame(200,self)

        self.load_config()
        self.start_process()
        self.getCourseInfo()
        self.initfun() 

    def windowinit(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setMouseTracking(True)

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
        if config["need_prompt"] == 'T':
            self.prompt_flag = True
        else:
            self.prompt_flag = False

    def getCourseInfo(self):
        #获取课程视频路径
        sql_path = """SELECT course_Path
                    FROM course_actionresponse
                    WHERE course_ID = {}""".format(self.course_id)
        self.course_path = self.db.search_table(sql_path)[0][0]
        
        self.video_ip, self.course_dir = self.get_ip()
        course_url = "http://" + self.video_ip + self.course_dir + self.course_path
        response = requests.get(course_url)
        self.course_path = './data/course_action/response/' + os.path.basename(self.course_path)
        
        if not os.path.exists(os.path.dirname(self.course_path)):
            os.makedirs(os.path.dirname(self.course_path))
        if not os.path.exists(self.course_path):
            with open(self.course_path, 'wb') as f:
                f.write(response.content)
        # 获取检查点信息
        sql_point = """SELECT point_ID, start_time, end_time, action_ID, Scene_Des
                        FROM point_actionresponse
                        WHERE course_ID = {}
                        ORDER BY start_time""".format(self.course_id)
        self.points = self.db.search_table(sql_point)
        # 勾拳 踢腿 勾拳 踢腿 闪躲 闪躲 提膝
        self.points_index = 0
        self.action_index = 0
    def initfun(self):
        self.play_flag = True
        self.num = 5
        
        self.show_timer = QtCore.QTimer()
        self.show_timer.timeout.connect(self.show_img)

        self.tip_timer = QtCore.QTimer()
        self.tip_timer.timeout.connect(self.change_num)
        self.timer_stamp = QtCore.QTimer()
        self.timer_stamp.timeout.connect(self.timecheck)
        self.timer_show = QtCore.QTimer()
        self.timer_show.timeout.connect(self.show_result)
        self.point_start_flag = True
        self.point_in_flag = False
        self.action_l = []
        self.tip_timer.start(1000)
        self.show_timer.start(20)
        
    def get_ip(self):
        json_path = "./data/dbconfig/database_account_password.json"
        with open(json_path) as f:
            data_base_json = json.load(f)        
        return data_base_json["video_ip"], data_base_json["course_dir"]
    

    def ready(self):
        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(self.videoWidget)
        media = QtCore.QUrl.fromLocalFile(self.course_path)
        self.player.setMedia(QMediaContent(media))
        self.player.play()
        self.timer_stamp.start(20)
        self.timer_show.start(25)

    def change_num(self):
        opacity = QGraphicsOpacityEffect()
        self.lab_tip.setStyleSheet("color: rgb(255, 255, 255);\n"
                                     "background-color: rgb(0, 0, 0);\n"
                                     "font: 100pt \"Pristina\";")
        if self.num > 0:
            # for i in range(self.num*10, self.num*10 - 10, -1):
            #     self.lab_tip.setText(str(self.num))
            #     self.lab_tip.repaint()
            self.lab_tip.setText(str(self.num))            
            opacity.setOpacity((self.num + 1) / 5 )
            self.lab_tip.setGraphicsEffect(opacity)
                # time.sleep(0.05)
            self.num -= 1
        elif self.num == 0:
            self.lab_tip.setText("开始！")
            self.lab_tip.repaint()
            self.num -=1
        else:
            self.lab_tip.hide()
            self.tip_timer.stop()
            self.ready()

    def show_result(self):
        action_class = {-1: '无动作',0: '勾拳', 1: '格挡', 2: '肘击', 3: '直拳',
                    4: '踢腿', 5: '提膝', 6: '戒备', 7: '闪躲'}
        # 直到取出最后一份结果再展示
        if self.acqueue.qsize() > 0:
            start, end, action, pro = self.acqueue.get()
            
            if pro > 0.5:
                self.action_l.append((start, end, action, pro))
                self.lab_info.setText(
                    "当前反应: {} \n建议反应: {}".format(action_class[action], 
                                             action_class[self.points[len(self.action_l) - 1][3]]))
            else:
                self.action_l.append((0, 0, -1, 1))
                self.lab_info.setText(
                    "当前反应: {} \n建议反应: {}".format(action_class[-1], 
                                             action_class[self.points[len(self.action_l) - 1][3]]))
            if pro > 0.5 and action == self.points[self.action_index][3]:
                self.hint_frame.show_green() 
            else:
                self.hint_frame.show_red()
            self.action_index += 1
        if (len(self.action_l) == len(self.points)) and\
            self.player.position() >= self.player.duration() - 10:
            self.timer_show.stop()
        else:
            return
        target = [self.points[i][3] for i in range(len(self.points))]
        self.result_ = Reaction_Result(self, target, self.action_l)
        self.result_.show()
    def show_img(self):
        if not self.using_sensor:
            img = self.imgqueue.get()
            pixmap = QPixmap.fromImage(
                QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888))
            pixmap = pixmap.scaled(self.lab_cam.width(), 
                                   self.lab_cam.height(), 
                                   QtCore.Qt.IgnoreAspectRatio)
            self.lab_cam.setPixmap(pixmap)
    def timecheck(self):
        
        if self.points_index == len(self.points) or not self.play_flag:
            self.timer_stamp.stop()
            return
    
        current_time = self.player.position()

        if current_time + 500 >= self.points[self.points_index][1] and self.point_start_flag:
            #提示检查点开始
            self.hint_frame.show_blue()
            self.point_start_flag = False
            if self.prompt_flag:
                self.lab_info.setText(self.points[self.points_index][4])

        if self.points[self.points_index][2] > current_time > self.points[self.points_index][1]:
            if self.point_in_flag:
                self.timequeue.put((current_time, 0))
                self.lab_info.setText('')
            else:
                self.timequeue.put((current_time, -2))
                self.point_in_flag = True
        if current_time >= self.points[self.points_index][2] and self.point_in_flag:
            self.timequeue.put((current_time, -1))
            self.point_in_flag = False
            self.point_start_flag = True
            self.points_index += 1


    def start_process(self):
        self.stop_event = Event()
        self.imgqueue = Queue(10)
        self.timequeue = Queue(10)
        self.corqueue = Queue(10)
        self.skqueue = Queue(10)
        self.acqueue = Queue(10)

        process_id = []
        if self.using_sensor:
            process_id.append(Process(target=parse_data, 
                                      args=(self.stop_event, 
                                            self.timequeue, 
                                            self.corqueue)))
        else:
            process_id.append(Process(target=skeleton_get,
                                      args=(self.stop_event, 
                                            self.timequeue,
                                            self.corqueue,
                                            self.imgqueue,
                                            self.camera)))
        process_id.append(Process(target=seg,
                                  args=(self.stop_event,
                                        self.corqueue, 
                                        self.skqueue))) 
        process_id.append(Process(target=actionRec, 
                                  args=(self.stop_event,
                                        self.skqueue,
                                        self.acqueue)))
        for i in process_id:
            i.daemon = True
            i.start()

    
    def exit(self, score):
        if score != 0:
            sql_upload = """INSERT grade_reaction
                            (student_ID, course_ID, grade, train_time)
                            VALUES(%s, %s, %s, %s)"""
            t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            args = [[self.student_id, self.course_id,  score, t]]
            self.db.insert_data(sql=sql_upload, args=args)                    
        self.show_timer.stop()
        self.player.stop()            
        self.stop_event.set()
        
        self.hint_frame.timer_end.stop()
        self.parent.show()
        self.hint_frame.close()
        # self.contral.close()
        self.close()
