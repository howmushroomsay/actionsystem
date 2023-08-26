from auxiliary_tools import process_bvhfile, process_bvhkeyframe, get_skdict
import cv2, json, socket
import numpy as np
import matplotlib.pyplot as plt
import time
from auxiliary_tools import skeleton_from_video

def skeleton_tran(c:np.ndarray):
    skeleton = np.zeros([25, 3])
    if c.shape[0] == 33:
        n = [-1, -1, -1, -1, 12, 14, 16, 22, 11, 13, 15, 21,
            24, 26, 28, 32, 23, 25, 27, 31, -1, 20, 22, 19, 21]
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
    elif c.shape[0] == 59:
        n = [0, 7, 11, 12,
             37, 38, 39, 39, 14, 15, 16, 16,
             4, 5, 6, 6, 1, 2, 3, 3,
             -1,
             39, 39, 16, 16]
        # n = [0, 7, 11, 12,
        #      14, 15, 16, 16, 37, 38, 39, 39,
        #      1, 2, 3, 3, 4, 5, 6, 6,
        #      -1,
        #      16, 16, 39, 39,]
        for i in range(3):
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

def read_data(last_data, data):
    data_ = last_data + data.decode()
    temp = data_.split('||')
    data_ = temp[0]
    last_data =  '||'.join(temp[1:])
    rotation = [float(i) for i in data_.split(' ')[5:-1]]
    return 0, rotation, last_data

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
        y1 = -int(skeleton[connect[i][0]][2]) + height
        x2 = int(skeleton[connect[i][1]][0]) + width
        y2 = -int(skeleton[connect[i][1]][2]) + height
        color = (255, 0, 0)
        thick = 10
        img = cv2.line(img, (x1,y1), (x2,y2), color, thickness=thick)
    # 画关节点
    for i in range(15):
        x = int(skeleton[i][0]) + width
        y = -int(skeleton[i][2]) + height
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
    img = cv2.imread('./data/empty.png')
    img = cv2.resize(img, (1920,1080))
    while not stop_event.is_set():
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
    
def load_json(json_path):
    with open(json_path, encoding='UTF-8') as f:
        data_json = json.load(f)
    return data_json
def draw_skeleton3d(stop_event, draw_queue):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    body = [[18, 17, 16, 0,],
             [0, 12, 13, 14],
            [0, 20, 2, 3],
            [11,10,9,8,20,],
             [20,4,5,6,7]]
    # body = [[6,5,4,0],[3,2,1,0],[0,13,14], [9,8,7,13],[13,10,11,12]]
    colors = ['g','b','m','y','k']
    while not stop_event.is_set():
        flag, skeleton = draw_queue.get()
        plt.cla()
        # ax.view_init(0, -120)
        # ax.view_init(90, -90)
        ax.set_xlim3d([-100, 100])
        ax.set_zlim3d([-100, 100])
        ax.set_ylim3d([-100, 100])
        ax.set_xlabel('xxx')
        ax.set_ylabel('yyy')
        ax.set_zlabel('zzz')
        x = skeleton[:, 0]
        z = skeleton[:, 2]
        y = skeleton[:, 1]
        # x = -skeleton[:, 0]
        # y = -skeleton[:, 2]
        # z = -skeleton[:, 1]
        for i in range(len(body)):
            part = body[i]
            color = colors[i]
            x_plot = x[part]
            y_plot = y[part]
            z_plot = z[part]
            ax.plot(x_plot, y_plot, z_plot, color=color,
                    marker='o', markerfacecolor='r')
        
        plt.pause(0.01)

def parse_data(stop_event, timequeue, corqueue, draw_queue=None):
    myskeleton = process_bvhfile('data/bvh/test.bvh')
    skeleton_dict, index_dict = get_skdict(path='data/bvh/a.txt')
    xyz_dict = {'Y':0, 'Z':1, 'X':2}
    client = socket.socket()
    port = int(load_json('./data/sensor/config.json')["port"])
    try:
        client.connect(("127.0.0.1", port))
    except:
        print('disconnect')
        return
    flag = 0
    last_data = ''
    l = []
    print('start  parse')
    while not stop_event.is_set():
        data = client.recv(3000)
        displacemenet, rotation, last_data = read_data(last_data, data)
        skeleton = np.zeros((59,3))
        if timequeue.qsize() > 0:
            t, flag = timequeue.get()
            process_bvhkeyframe(rotation, myskeleton.root, 0)
            header, frames = myskeleton.get_frames_worldpos()
            for j in range(1, len(frames)):
                name = header[j].split('.')
                k = skeleton_dict[name[0]]
                m = xyz_dict[name[1]]
                skeleton[k][m] = frames[j]
            skeleton_ = skeleton_tran(skeleton) / 10
            # skeleton_[:,0] = -skeleton_[:,0]
            # skeleton_[:,1] = -skeleton_[:,1]
            # skeleton_[:,2] = -skeleton_[:,2]
            # l.append(skeleton_)
            # if(len(l) > 300):
            #     np.save('sensor.npy', np.stack(l))
            #     print('ok')
            #     break
            draw_queue.put((flag, skeleton_))

from multiprocessing import Event, Queue, Process
# def draw_3d(skeleton, skeleton2):
#     frame = max(skeleton.shape[0], skeleton2.shape[0])
    

#     fig = plt.figure()

#     ax = fig.add_subplot(121,projection='3d')
#     ax2 = fig.add_subplot(122,projection='3d')
#     # ax.axis('off')
#     # ax.grid(None)

#     for i in range(0, frame, 2):
#         if i < skeleton.shape[0]:
#             ax.cla()
#             skeleton_ = skeleton_trans_ntu(skeleton[i])
#             ax.set_xlim3d([-1, 1])
#             ax.set_ylim3d([-1, 1])
#             ax.set_zlim3d([-0.2, 1.8])
#             ax.set_xlabel('xxx')
#             ax.set_ylabel('yyy')
#             ax.set_zlabel('zzz')
#             x = -skeleton_[:, 0]
#             y = -skeleton_[:, 2]
#             z = skeleton_[:, 1]

#             body = [[0,13,14], [6,5,4,0,1,2,3],[12,11,10,13,7,8,9]]
#             for part in body:
#                 x_plot = x[part]
#                 y_plot = y[part]
#                 z_plot = z[part]
#                 ax.plot(x_plot, y_plot, z_plot, color='b',
#                         marker='o', markerfacecolor='r')
#         if i*3 < skeleton2.shape[0]:
#             ax2.cla()
#             skeleton_ = skeleton_trans_ntu(skeleton2[i*3])
#             ax2.set_xlim3d([-1, 1])
#             ax2.set_ylim3d([-1, 1])
#             ax2.set_zlim3d([-0.2, 1.8])
#             ax2.set_xlabel('xxx')
#             ax2.set_ylabel('yyy')
#             ax2.set_zlabel('zzz')
#             x = skeleton_[:, 0]
#             y = skeleton_[:, 1]
#             z = skeleton_[:, 2]

#             body = [[0,13,14], [6,5,4,0,1,2,3],[12,11,10,13,7,8,9]]
#             for part in body:
#                 x_plot = x[part]
#                 y_plot = y[part]
#                 z_plot = z[part]
#                 ax2.plot(x_plot, y_plot, z_plot, color='b',
#                         marker='o', markerfacecolor='r')
        
#         plt.pause(0.001)


# skeleton = np.load('./T.npy')
# skeleton2 = np.load('./S17.npy')
 

if __name__ == "__main__":
    stop_event = Event()
    timequeue = Queue(10)
    corqueue = Queue(10)
    drawqueue = Queue(10)

    process_id = []
    process_id.append(Process(target=parse_data,
                                      args=(stop_event,
                                            timequeue, 
                                            corqueue, 
                                            drawqueue)))
    process_id.append(Process(target=draw_skeleton2d, 
                                args=(stop_event, 
                                    drawqueue)))
    
    # for i in process_id:
    #     i.daemon = True
    #     i.start()
    process_id[0].daemon = True
    process_id[0].start()
    process_id[1].daemon = True
    process_id[1].start()
    # skeleton = skeleton_from_video('2.mp4')
    # np.save('video.npy', np.stack(skeleton))
    
    skeleton = np.load('video.npy')*100 
    # skeleton = np.load('sensor.npy')*100
    # draw_3d(skeleton1, skeleton2)
    # print("hhh")
    i =0
    while(1):
        # drawqueue.put((0, skeleton[i]))
        # i+=1
        # i%=skeleton.shape[0]
        timequeue.put((0,0))
        if corqueue.qsize():
            corqueue.get()


