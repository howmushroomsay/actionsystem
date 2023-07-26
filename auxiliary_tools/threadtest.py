import threading
import cv2
import torch, time
import mediapipe as mp
import numpy as np
from easydict import EasyDict as edict
from .action_model.action_rec import get_parameters
from .action_model.src.processor import Processor
# from skeleton_process.lib.camera import uv2xyz_ourcamera
# from skeleton_process.lib.camera_param import camera_param
pose = mp.solutions.pose.Pose(static_image_mode=False,
                              model_complexity=1,
                              smooth_landmarks=True,
                              enable_segmentation=True,
                              min_detection_confidence=0.5,
                              min_tracking_confidence=0.5)


def process1(img, c):
    neighbor_2base = np.array([(7, 3), (3, 2), (2, 1), (1, 0), (0, 4), (4, 5), (5, 6), (6, 8), (9, 10),
                               (11, 12), (11, 23), (23, 24), (24, 12),
                               (11, 13), (13, 15), (15, 21), (15,
                                                              19), (15, 17), (17, 19),
                               (12, 14), (14, 16), (16, 22), (16,
                                                              20), (16, 18), (18, 20),
                               (23, 25), (25, 27), (27, 31), (27, 29), (31, 29),
                               (24, 26), (26, 28), (28, 30), (28, 32), (30, 32)])
    w = img.shape[1]
    h = img.shape[0]
    for i in range(33):
        cx = int(c[i][0]*w)
        cy = int(c[i][1]*h)
        img = cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)
    for i in range(35):
        a = neighbor_2base[i][0]
        b = neighbor_2base[i][1]
        cx_0 = int(c[a][0]*w)
        cy_0 = int(c[a][1]*h)
        cx_1 = int(c[b][0]*w)
        cy_1 = int(c[b][1]*h)
        img = cv2.line(img, [cx_0, cy_0], [cx_1, cy_1], (255, 255, 255), 3)
    return img


def skeleton_tran(c):
    n = [-1, -1, -1, -1, 12, 14, 16, 22, 11, 13, 15, 21,
         24, 26, 28, 32, 23, 25, 27, 31, -1, 20, 22, 19, 21]
    skeleton = np.zeros([25, 3])
    for i in range(3):
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
    return skeleton


# def get2dpose(img):
#     img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     h, w = img.shape
#     results = pose.process(img_RGB)
#     keypoints_2d = np.zeros(shape=(33, 2))
#     if results.pose_landmarks:
#         for i in range(33):
#             keypoints_2d[i][0] = results.pose_landmarks.landmark[i].x * w
#             keypoints_2d[i][1] = results.pose_landmarks.landmark[i].y * h
#     return keypoints_2d


# def get3dpose(pose2d_1, pose2d_2):
#     keypoints_3d = np.zeros((33, 3))
#     for j in range(33):
#         keypoints_3d[j] = uv2xyz_ourcamera(lx=pose2d_1[1][j][0], ly=pose2d_1[1][j][1],
#                                            rx=pose2d_2[1][j][0], ry=pose2d_2[1][j][1],
#                                            camera_param=camera_param).squeeze()
#     return keypoints_3d


class Action_Recognizer(Processor):
    def __init__(self):
        args = get_parameters(2001)
        super().__init__(args)
        skeleton_test = np.zeros([3, 200, 25, 1])
        skeleton_test = torch.tensor(skeleton_test)
        self.eval(skeleton_test)
        self.action_class = {0: '出拳', 1: '格挡', 2: '肘击', 3: '出拳',
                                4: '踢腿', 5: '提膝', 6: '戒备', 7: '闪躲'}


class camera_thread(threading.Thread):
    def __init__(self, stop_event, timequeue, imgqueue, camera1=0, camera2=None):
        super().__init__()
        self.timequeue = timequeue
        self.q = imgqueue
        self.stop_event = stop_event
        try:
            self.cap1 = cv2.VideoCapture(camera1)
            self.cap2 = cv2.VideoCapture(camera2) if camera2 else None
        except:
            print('error camera')

    def run(self):
        if self.cap2:
            while not self.stop_event.is_set():
                if self.timequeue.qsize() > 0:
                    t, flag = self.timequeue.get()
                    ret1, img1 = self.cap1.read()
                    ret2, img2 = self.cap2.read()
                    if ret1 and ret2:
                        self.q.put((t, img1, img2, flag))
            pass
        else:
            while not self.stop_event.is_set():
                if self.timequeue.qsize() > 0:
                    t, flag = self.timequeue.get()
                    ret, img = self.cap1.read()
                    if ret:
                        self.q.put((t, img, flag))

class skeleton_single_Thread(threading.Thread):
    def __init__(self, stop_event, timequeue, corqueue):
        super().__init__()
        self.timequeue = timequeue
        self.co_queue = corqueue
        self.stop_event = stop_event
        self.cap = cv2.VideoCapture(0)


    def run(self):
        while not self.stop_event.is_set():
            time1 = time.time()
            if self.timequeue.qsize() > 0:
                t, flag = self.timequeue.get()
                ret, img = self.cap.read()
                cv2.imshow('ggg',img)
                cv2.waitKey(1)
                print('read time:',time.time() - time1)
                img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = pose.process(img_RGB)
                skeleton = np.zeros((33, 3))
                if results.pose_world_landmarks:
                    for i in range(33):
                        skeleton[i][0] = results.pose_world_landmarks.landmark[i].x
                        skeleton[i][1] = results.pose_world_landmarks.landmark[i].y
                        skeleton[i][2] = results.pose_world_landmarks.landmark[i].z

                skeleton = skeleton_tran(skeleton)
                print('process time:',time.time() - time1)
                self.co_queue.put((t, skeleton, flag))
# class skeletonGet2_thread(threading.Thread):
#     def __init__(self, stop_event, imgqueue, corqueue):
#         super().__init__()
#         self.stop_event = stop_event
#         self.img_queue = imgqueue
#         self.co_queue = corqueue

#     def run(self):
#         while not self.stop_event.is_set():
#             if self.img_queue.qsize() > 0:
#                 t, img1, img2, flag = self.img_queue.get()
#                 pose2d_1 = get2dpose(img1)
#                 pose2d_2 = get2dpose(img2)
#                 skeleton = np.zeros((25, 3))
#                 if np.any(pose2d_1) and np.any(pose2d_2):
#                     pose3d = get3dpose(pose2d_1, pose2d_2)
#                     skeleton = skeleton_tran(pose3d)
#                 self.co_queue.put((t, skeleton, flag))


class skeletonGet_thread(threading.Thread):
    def __init__(self, stop_event, imgqueue, corqueue):
        super().__init__()
        self.stop_event = stop_event
        self.img_queue = imgqueue
        self.co_queue = corqueue

    def run(self):
        while not self.stop_event.is_set():

            if self.img_queue.qsize() > 0:
                t, img, flag = self.img_queue.get()
                img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = pose.process(img_RGB)
                skeleton = np.zeros((33, 3))
                if results.pose_world_landmarks:
                    for i in range(33):
                        skeleton[i][0] = results.pose_world_landmarks.landmark[i].x
                        skeleton[i][1] = results.pose_world_landmarks.landmark[i].y
                        skeleton[i][2] = results.pose_world_landmarks.landmark[i].z

                skeleton = skeleton_tran(skeleton)
                self.co_queue.put((t, skeleton, flag))


class skSeg_thread(threading.Thread):
    def __init__(self, stop_event, corqueue, skeletonqueue):
        super().__init__()
        self.stop_event = stop_event
        self.co_queue = corqueue
        self.sk_queue = skeletonqueue

        seg_arg = edict()
        """
        window： 求方差的窗口大小
        min_action： 动作持续的最短时间
        var_threshold1：动作烈度较低时的方差阈值
        var_threshold2：动作烈度较高时的方差阈值
        var_diff_threshold：判断动作烈度的阈值
        """
        seg_arg.window = 10
        seg_arg.min_action = 5
        seg_arg.var_threshold = 300
        # seg_arg.var_threshold1 = 300
        # seg_arg.var_threshold2 = 400
        seg_arg.var_diff_threshold = 800
        self.args = seg_arg

    def run(self):
        args = self.args

        sk_list, t_list = [], []
        stop_flag = True
        var_threshold = args.var_threshold
        count = 0
        first_action = True

        while not self.stop_event.is_set():
            if self.co_queue.empty():
                continue
            t, skeleton, t_flag = self.co_queue.get()
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
                if count - start - 5 <= args.min_action:
                    # 重置动作起始标志
                    print('动作长度不够')
                    stop_flag = True
                    # self.sk_queue.put((0, 0, 0))
                # 正常结束
                else:
                    end = count - 5
                    end_time = t_list[end]
                    skeleton_n = np.zeros([1, 200, 25, 3])
                    # print(1, end - start)
                    skeleton_n[0, :end-start, :,
                               :] = np.array(sk_list[start:end])
                    skeleton_n = skeleton_n.transpose(3, 1, 2, 0)
                    # self.sk_queue.put((skeleton_n, start_time, end_time))

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
                        skeleton_n[0, :end-start, :,
                                   :] = np.array(sk_list[start:end])
                        skeleton_n = skeleton_n.transpose(3, 1, 2, 0)
                        # self.sk_queue.put((skeleton_n, start_time, end_time))
                        stop_flag = True
                        # 当前区间骨架分割完毕，等待下一区间，回到初始状态
                        first_action = False
                        count = 0
                        sk_list = []
                        t_list = []


class actionRec_thread(threading.Thread):
    def __init__(self, stop_event, skeletonqueue, actionqueue):
        super().__init__()
        self.stop_event = stop_event
        self.sk_queue = skeletonqueue
        self.ac_queue = actionqueue
        self.Action = Action_Recognizer()
        self.action_class = {-1: '无动作', 0: '出拳', 1: '格挡', 2: '肘击', 3: '出拳',
                                4: '踢腿', 5: '提膝', 6: '戒备', 7: '闪躲'}
    def run(self):
        while not self.stop_event.is_set():
            if self.sk_queue.qsize() > 0:
                skeleton, start, end = self.sk_queue.get()
                if not(end):
                    pro, action = 0, -1
                    self.ac_queue.put((start, end, action, pro))
                else:
                    skeleton = torch.tensor(skeleton)
                    pro, action = self.Action.eval(skeleton)
                    self.ac_queue.put((start, end, action, pro))
                print(start, end, self.action_class[action], pro)
