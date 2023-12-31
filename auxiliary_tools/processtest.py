import cv2, json
import torch
import socket
import logging
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from easydict import EasyDict as edict
from .bvh_process import cal_pos, ProcessBVH, get_skdict
from .action_model.action_rec import get_parameters
from .action_model.src.processor import Processor

pose = mp.solutions.pose.Pose(static_image_mode=False,
                              model_complexity=0,
                              smooth_landmarks=True,
                              enable_segmentation=True,
                              min_detection_confidence=0.5,
                              min_tracking_confidence=0.5)
def load_json(json_path):
    with open(json_path, encoding='UTF-8') as f:
        data_json = json.load(f)
    return data_json

def skeleton_tran(c:np.ndarray):
    skeleton = np.zeros([25, c.shape[1]])
    if c.shape[0] == 33:
        n = [-1, -1, -1, -1, 12, 14, 16, 22, 11, 13, 15, 21,
            24, 26, 28, 32, 23, 25, 27, 31, -1, 20, 22, 19, 21]  
        for i in range(c.shape[1]):
            skeleton[0][i] = (c[23][i] + c[24][i]) / 2
            skeleton[1][i] = (c[11][i] + c[12][i] + c[23][i] + c[24][i]) / 4
            skeleton[2][i] = (c[9][i] + c[10][i] + c[11][i] + c[12][i]) / 4
            skeleton[3][i] = (c[1][i] + c[4][i]) / 2
            skeleton[20][i] = (c[11][i] + c[12][i]) / 2
        for i in range(25):
            if n[i] != -1:
                skeleton[i] = c[n[i]]
        a = skeleton[0].copy()
        for i in range(25):
            skeleton[i] -= a
    elif c.shape[0] == 59:
        # n = [0, 7, 11, 12,
        #      37, 38, 39, 39, 14, 15, 16, 16,
        #      4, 5, 6, 6, 1, 2, 3, 3,
        #      -1,
        #      39, 39, 16, 16]
        n = [0, 7, 11, 12,
             14, 15, 16, 16, 37, 38, 39, 39,
             1, 2, 3, 3, 4, 5, 6, 6,
             -1,
             16, 16, 39, 39,]
        for i in range(c.shape[1]):
            skeleton[20][i] = (c[13][i] + c[36][i]) / 2
        for i in range(25):
            if n[i] != -1:
                skeleton[i] = c[n[i]]
        for i in range(25):
            # 转换成米为单位
            skeleton[i] = skeleton[i] / 10
        a = skeleton[0].copy()
        for i in range(25):
            skeleton[i] -= a
    return skeleton

class Action_Recognizer(Processor):
    def __init__(self):
        args = get_parameters(2001)
        super().__init__(args)
        skeleton_test = np.zeros([3, 200, 25, 1])
        skeleton_test = torch.tensor(skeleton_test)
        self.eval(skeleton_test)
        self.action_class = {0: '勾拳', 1: '格挡', 2: '肘击', 3: '直拳',
                                4: '踢腿', 5: '提膝', 6: '戒备', 7: '闪躲'}


def read_data(last_data, data):
    data_ = last_data + data.decode()
    temp = data_.split('||')
    data_ = temp[0]
    last_data =  '||'.join(temp[1:])
    rotation = [float(i) for i in data_.split(' ')[5:-1]]
    return 0, rotation, last_data

def draw(img, skeleton):

    index = [-1, 24, 26, 28, 23, 25, 27, 12, 14, 16, 11, 13, 15,-1, 0]
    skeleton_ = np.zeros([int(len(index)), 3])
    for i in range(len(index)):
        skeleton_[i] = skeleton[index[i]]
    for i in range(3):
        skeleton_[0][i] = (skeleton[23][i] + skeleton[24][i]) / 2
        skeleton_[13][i] = (skeleton[11][i] + skeleton[12][i]) / 2
    for i in range(len(index)):
        skeleton_[i][0] *= img.shape[1]
        skeleton_[i][1] *= img.shape[0]        
    connect = [[6,5],[5,4],[4,0],[0,1],[1,2],[2,3],
                [0,13],[13,14],
                [12,11],[11,10],[10,13],[13,7],[7,8],[8,9]]
    for i in range(len(connect)):
        point1 = [int(skeleton_[connect[i][0]][0]), int(skeleton_[connect[i][0]][1])]
        point2 = [int(skeleton_[connect[i][1]][0]), int(skeleton_[connect[i][1]][1])]
        cv2.line(img, point1, point2, (255,0,0), 5)
    for i in range(len(index)):
        cv2.circle(img, (int(skeleton_[i][0]), int(skeleton_[i][1])), 10, (0,0,255), -1)
    return img

def skeleton_get(stop_event, timequeue, corqueue, imgqueue=None, count_queue=None, camera=0, action_train=True):
    logging.info('skeleton_get process start')
    cap = cv2.VideoCapture(camera)
    ret, img = cap.read()
    if not ret:
        logging.error('camera error')
        stop_event.set()
        return
    while not stop_event.is_set():
        if action_train:
            skeleton = np.zeros((33,3))
        else:
            skeleton = np.zeros((33,4))
        skeleton_img = np.zeros((33,3))
        ret, img = cap.read()
        if not ret:
            logging.error('camera error')
            stop_event.set()
            break
        img = cv2.resize(img, (1920, 1080))
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if imgqueue != None:
            imgqueue.put(img_RGB)
        # img = cv2.flip(img, 1)
        if timequeue.qsize() > 0:
            t, flag = timequeue.get()
            if count_queue != None:
                count_queue.put((flag,cv2.resize(img_RGB, (480, 360))))
            if not action_train:                
                if(flag == 1):
                    cv2.destroyWindow('Student Pose')
                    continue
                elif(flag==2):
                    break
            
            results = pose.process(img_RGB)
            if results.pose_world_landmarks:
                for i in range(33):
                    skeleton[i][0] = results.pose_world_landmarks.landmark[i].x
                    skeleton[i][1] = results.pose_world_landmarks.landmark[i].y
                    skeleton[i][2] = results.pose_world_landmarks.landmark[i].z
                    if not action_train:
                        skeleton[i][3] = results.pose_world_landmarks.landmark[i].visibility
            # 用于规范训练画图
            if not action_train:
                if results.pose_world_landmarks:
                    for i in range(33):
                        skeleton_img[i][0] = results.pose_landmarks.landmark[i].x
                        skeleton_img[i][1] = results.pose_landmarks.landmark[i].y
                        skeleton_img[i][2] = results.pose_landmarks.landmark[i].z
                # img = cv2.resize(img,(1920,1080))
                img = draw(img, skeleton_img)
                img = cv2.resize(img, (480, 270))
                # img = cv2.flip(img, 1)
                
                cv2.namedWindow('Student Pose', cv2.WINDOW_AUTOSIZE)
                cv2.resizeWindow('Student Pose', 480, 270)
                cv2.moveWindow('Student Pose', 1440, 0)
                cv2.setWindowProperty('Student Pose', cv2.WND_PROP_TOPMOST, 1)
                cv2.imshow('Student Pose', img)
                cv2.waitKey(1)

            #33节点骨架转25节点骨架
            skeleton_ = skeleton_tran(skeleton)
            corqueue.put((t, skeleton_, flag))
    cap.release()
    logging.info('skeleton_get process end')

def draw_empty(img, skeleton):
    skeleton = skeleton * 500
    width = img.shape[1] // 2
    height = img.shape[0] // 2
    # 骨架连接关系
    # connect = [[18,17],[17,16],[16,0],[0,12],[12,13],[13,14],
    #            [0,20],[20,3],
    #            [10,9],[9,8],[8,20],[20,4],[4,5],[5,6]]
    connect = [[6,5],[5,4],[4,0],[0,1],[1,2],[2,3],
                [0,13],[13,14],
                [12,11],[11,10],[10,13],[13,7],[7,8],[8,9]]
    # 画骨架
    for i in range(len(connect)):
        x1 = int(skeleton[connect[i][0]][0]) + width
        y1 = int(skeleton[connect[i][0]][1]) + height
        x2 = int(skeleton[connect[i][1]][0]) + width
        y2 = int(skeleton[connect[i][1]][1]) + height
        color = (255, 0, 0)
        thick = 10
        img = cv2.line(img, (x1,y1), (x2,y2), color, thickness=thick)
    # 画关节点
    for i in range(15):
        x = int(skeleton[i][0]) + width
        y = int(skeleton[i][1]) + height
        radius = 15
        color = (0, 0, 255)
        thick = -1
        img = cv2.circle(img, (x,y) , radius, color, thick)
    return img

def skeleton_trans_ntu(landmarks):
    # 将25节点的ntu骨架转换成需要计算的15个关键点
    visibility = landmarks.shape[1]
    index = [0, 12, 13, 14, 16, 17, 18, 4, 5, 6, 8, 9, 10, 20, 3]
    skeleton = np.zeros([int(len(index)), visibility])
    for i in range(len(index)):
        skeleton[i] = landmarks[index[i]]
    return skeleton

def draw_skeleton2d(stop_event, draw_queue):
    logging.info("draw_skeleton2d process start")
    img = cv2.imread('./data/empty.png')
    img = cv2.resize(img, (1920,1080))
    while not stop_event.is_set():
        if draw_queue.qsize() > 0:
            flag, skeleton = draw_queue.get()             
            if(flag == 1):
                cv2.destroyWindow('Student Pose')
                continue
            elif(flag==2):
                break
            
            skeleton = skeleton_trans_ntu(skeleton)
            img1 = draw_empty(img.copy(), skeleton)
            img1 = cv2.resize(img1, (480, 270))
            cv2.namedWindow('Student Pose', cv2.WINDOW_AUTOSIZE)
            cv2.resizeWindow('Student Pose', 480, 270)
            cv2.moveWindow('Student Pose', 1440, 0)
            cv2.setWindowProperty('Student Pose', cv2.WND_PROP_TOPMOST, 1)
            cv2.imshow('Student Pose', img1)
            cv2.waitKey(1)
    logging.info("draw_skeleton2d process end")    
def draw_skeleton3d(stop_event, draw_queue):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    body = [[18, 17, 16, 0, 12, 13, 14],
            [0, 20, 2, 3],
            [11,10,9,8,20,4,5,6,7]]
    img = cv2.imread('./data/empty.png')
    while not stop_event.is_set():
        skeleton = draw_queue.get()
        plt.cla()
        ax.view_init(0, -120)
        ax.set_xlim3d([-100, 100])
        ax.set_zlim3d([-100, 100])
        ax.set_ylim3d([-100, 100])
        x = skeleton[:, 0]
        y = skeleton[:, 1]
        z = skeleton[:, 2]
        for part in body:
            x_plot = x[part]
            y_plot = y[part]
            z_plot = z[part]
            ax.plot(x_plot, z_plot, y_plot, color='b',
                    marker='o', markerfacecolor='r')
        plt.pause(0.01)

    plt.close("all")

def parse_data(stop_event, timequeue, corqueue, draw_queue=None):
    filename = "./data/bvh/test.bvh"
    joints, joints_offsets, joints_hierarchy = ProcessBVH(filename)
    temp = load_json("./data/sensor/config.json")
    ip_ = temp["ip"]
    port = int(temp['port'])
    try:
        client = socket.socket()
        client.connect((ip_, port))
    except:
        logging.error('sensor connect error')
        stop_event.set()
        return
    last_data = ""
    logging.info("parse_data processs start")
    while not stop_event.is_set():
        data = client.recv(3000)
        rotation, last_data = read_data(last_data, data)

        skeleton = np.zeros((59,3))
        if timequeue.qsize() > 0:
            t, flag = timequeue.get()
            skeleton = cal_pos(joints, joints_offsets, joints_hierarchy, rotation)
            skeleton_ = skeleton_tran(skeleton) / 10
            temp = skeleton_[:,1].copy()
            skeleton_[:,0] = skeleton_[:,0]
            skeleton_[:,1] = -skeleton_[:,1]
            skeleton_[:,2] = -skeleton_[:,-1]
            corqueue.put((t, skeleton_, flag))
            if draw_queue != None:
                draw_queue.put((flag, skeleton_))
    logging.info('parse_data process end')
def seg(stop_event, corqueue, skqueue):
    """
    window： 求方差的窗口大小
    min_action： 动作持续的最短时间
    var_threshold1：动作烈度较低时的方差阈值
    var_threshold2：动作烈度较高时的方差阈值
    var_diff_threshold：判断动作烈度的阈值
    """
    logging.info("seg process start")
    seg_arg = edict()
    seg_arg.window = 10
    seg_arg.min_action = 15
    seg_arg.var_threshold = 300
    # seg_arg.var_threshold1 = 300
    # seg_arg.var_threshold2 = 400
    seg_arg.var_diff_threshold = 800
    args = seg_arg
    sk_list, t_list = [], []
    stop_flag = True
    var_threshold = args.var_threshold
    count = 0
    first_action = True
    while not stop_event.is_set():
        if corqueue.empty():
            continue
        t, skeleton, t_flag = corqueue.get()
        # 判断是否已经进行了一次动作识别
        # 若已经进行了一次识别，舍弃这一检查点区间中余下的骨架数据
        if not first_action:
            if t_flag == -2:
                first_action = True
            else:
                continue

        sk_list.append(skeleton)
        t_list.append(t)
        count += 1
        
        # 区间开始,初始化start
        if t_flag == -2:
            start = 0 
            start_time = t_list[start]

        # 区间结束,若已经进行一次识别,不作处理
        # 未进行识别,截断序列,进行动作识别
        if t_flag == -1:
            
            if count - start - 5 <= args.min_action or start < 5:
                # 重置动作起始标志
                logging.info("动作长度不够")
                stop_flag = True
                skqueue.put((0, 0, 0))
            # 正常结束
            else:
                end = count - 5
                end_time = t_list[end]
                skeleton_n = np.zeros([1, 200, 25, 3])
                # print(1, end - start)
                skeleton_n[0, :end-start, :,:] = np.array(sk_list[start:end])
                skeleton_n = skeleton_n.transpose(3, 1, 2, 0)
                skqueue.put((skeleton_n, start_time, end_time))

            # 等待下一区间，回到初始状态
            count = 0
            sk_list = []
            t_list = []

        # 通过方差判断动作是否结束
        if count >= args.window:
            sk_temp = np.array(sk_list[-args.window:]) * 100
            var = 0
            for i in range(sk_temp.shape[1]):
                for j in range(sk_temp.shape[2]):
                    var += sk_temp[:, i, j].var()
            # print(var)
            # 动作开始
            if var > var_threshold and stop_flag:
                start = count - 5
                start_time = t_list[start]
                stop_flag = False

            # 动作结束
            elif var < var_threshold and not stop_flag:
                # 持续时间过短，不认为是完整动作，不进行识别
                if count - start - 5 <= args.min_action:
                    # 重置动作起始标志，保留部分骨架数据
                    stop_flag = True
                    count = args.window-1
                    sk_list = sk_list[-args.window+1:]
                    t_list = t_list[-args.window+1:]

                # 正常结束
                else:
                    end = count - 5
                    end_time = t_list[end]
                    skeleton_n = np.zeros([1, 200, 25, 3])
                    # print(2, end - start)
                    skeleton_n[0,:end-start,:,:] = np.array(sk_list[start:end])
                    skeleton_n = skeleton_n.transpose(3, 1, 2, 0)
                    skqueue.put((skeleton_n, start_time, end_time))
                    stop_flag = True
                    # 当前区间骨架分割完毕，等待下一区间，回到初始状态
                    first_action = False
                    count = 0
                    sk_list = []
                    t_list = []
    logging.info("seg process end")
def actionRec(stop_event, skqueue, acqueue):
    logging.info("actionRec process start")
    Action = Action_Recognizer()
    action_class = {-1: '无动作',0: '勾拳', 1: '格挡', 2: '肘击', 3: '直拳',
                    4: '踢腿', 5: '提膝', 6: '戒备', 7: '闪躲'}
    while not stop_event.is_set():
        if skqueue.qsize() > 0:
            skeleton, start, end = skqueue.get()
            if not(end):
                pro, action = 0, -1
                acqueue.put((start, end, action, pro))
            else:
                skeleton = torch.tensor(skeleton)
                pro, action = Action.eval(skeleton)
                acqueue.put((start, end, action, pro))
            logging.info((start, end, action_class[action], pro))
    logging.info("actionRec process end")
            