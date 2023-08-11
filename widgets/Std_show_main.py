import sys,cv2

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtGui

from .ui import Ui_Action_Eval

def draw(img, skeleton, erro_part=[]):
    # img: 1920*1080*3大小的图片
    # skeleton：ndarray大小(15*3)
    #           骨架的像素坐标，此处取髋关节为中心，人竖直站立头朝向为y正方向
    #           右手方向为x正方向 
    #           比例为真实坐标1m长度转换成1920*1080图上600个像素
    #           长度。
    # error_part: 错误位置, 四肢部分0,1,2,3: 左手，右手，左脚，右脚
    #
    # 在传入图片上进行15节点骨架的作图，正确节点使用绿色点位标出，
    # 错误点位在绿色点位基础上使用更大的红色圆圈标出
    gps_idx = { "左腿" : 3,
                "右腿" : 2,
               "左胳膊" : 1,
               "右胳膊" : 0
               }
    skeleton = skeleton * 600
    width = img.shape[1] // 2
    height = img.shape[0] // 2
    # 骨架连接关系
    connect = [[6,5],[5,4],[4,0], #右腿
               [0,1],[1,2],[2,3], #左腿
               [0,13],[13,14],
               [12,11],[11,10],[10,13], #右手
               [13,7],[7,8],[8,9]] #左手
    # 画骨架
    for i in range(len(connect)):
        x1 = int(skeleton[connect[i][0]][0]) + width
        y1 = int(skeleton[connect[i][0]][1]) + height
        x2 = int(skeleton[connect[i][1]][0]) + width
        y2 = int(skeleton[connect[i][1]][1]) + height
        color = (0, 255, 0)
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

    # 标注错误关节点位置
    error_joint = [[7, 8, 9],
                     [10, 11, 12],
                     [1, 2, 3],
                     [4, 5, 6]]
    for i in erro_part:
        i = gps_idx[i]
        for joint in error_joint[i]:
            x = int(skeleton[joint][0]) + width
            y = int(skeleton[joint][1]) + height
            radius = 25
            color = (255, 0, 0)
            thick = 4
            img = cv2.circle(img, (x,y) , radius, color, thick)
    return img

#一个画面展示教练骨架，一个画面展示学员骨架
class Std_show(QWidget, Ui_Action_Eval):
    # def __init__(self, parent, S_skeleton, T_skeleton, ) -> None:
    def __init__(self, parent, S_skeleton, T_skeleton, score, error_part=[]) -> None:
        # parent: 父界面
        # db: 数据库
        # S_skeleton: 学员骨架 list[ndarray]
        # T_skeleton: 教练骨架 list[ndarray]
        # score：得分
        # error_part: 错误位置 list[list[int]], 四肢部分0,1,2,3: 左手，右手，左脚，右脚
        super(Std_show, self).__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        assert(len(S_skeleton) == len(T_skeleton))
        
        self.setupUi(self)
        self.parent = parent
        self.score = score
        self.S_skeleton = S_skeleton
        self.T_skeleton = T_skeleton
        self.error_part = error_part
        self.img = cv2.imread('./data/empty.png')
        self.img = cv2.resize(self.img, (1920,1080))
        self.init_fun()
    
    def init_fun(self):
        self.btn_right.clicked.connect(self.nextframe)
        self.btn_left.clicked.connect(self.preframe)
        self.btn_back.clicked.connect(self.exit)
        self.btn_upload.clicked.connect(self.upload)

        self.lab_text.setText('您本次的训练成绩为: {}'.format(self.score))
        self.index = 0
        self.show_skeleton()
    
    def draw_left(self):
        # 将教练骨架展示在界面左侧
        skeleton = self.T_skeleton[self.index]
        left_skeleton = draw(self.img.copy(), skeleton.copy())
        show = cv2.resize(left_skeleton, (768, 432))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.lab_right_fig.setPixmap(QtGui.QPixmap.fromImage(showImage))
        self.lab_right_fig.setScaledContents(True)

    def draw_right(self):
        # 将学员骨架展示在界面右侧
        skeleton = self.S_skeleton[self.index]
        right_skeleton = draw(self.img.copy(), skeleton.copy(), [self.error_part[self.index]])
        self.lab_info.setText("{}不标准，注意改正".format(self.error_part[self.index]))
        show = cv2.resize(right_skeleton, (768, 432))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.lab_left_fig.setPixmap(QtGui.QPixmap.fromImage(showImage))
        self.lab_left_fig.setScaledContents(True)

    def show_skeleton(self):
        self.draw_left()
        self.draw_right()
    
    def preframe(self):
        self.index = (self.index + len(self.S_skeleton) - 1) % len(self.S_skeleton)
        self.show_skeleton()

    def nextframe(self):
        self.index = (self.index + len(self.S_skeleton) + 1) % len(self.S_skeleton)
        self.show_skeleton()

    def exit(self):
        self.close()        
        self.parent.back()

        
    def upload(self):
        self.close()        
        self.parent.upload()
        self.parent.back()


if __name__ == '__main__':
    # skeleton = read_skeleton('./test.skeleton')

    app = QApplication(sys.argv)
    win = Std_show(0, 0, 0)
    win.show()
    sys.exit(app.exec_())
