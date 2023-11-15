import os
import sys
import datetime
from PyQt5.QtWidgets import QApplication
from widgets import *
from auxiliary_tools import DatabaseOperation

import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./data/log.txt',
                    filemode='a')

logging.info("WELCOME TO THE SYSTEM")
import multiprocessing
if __name__ == "__main__":
    
    
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    # win = LogMain()
    student_id = int(sys.argv[1])
    window_type = int(sys.argv[2])

    # win = Reaction_Train_Main(0, 0, 0, using_sensor=)

    db = DatabaseOperation()
    if window_type == 0:
        logging.info("student{} start std_train".format(student_id))
        win = Center_Menu_Main(db, student_id, True)
    else:
        logging.info("student{} start reaction_train".format(student_id))
        win = Center_Menu_Main(db, student_id, False)
    # camera = "rtsp://admin:nvidia001@192.168.1.64/Streaming/Channels/1"
    win.show()
    code = app.exec_()
    
    for course_dir in os.listdir('./data/course_action'):
        course_dir = os.path.join('./data/course_action', course_dir)
        if not os.path.isdir(course_dir):
            continue
        for file in os.listdir(course_dir):
            path_ = os.path.join(course_dir, file)
            if os.path.isdir(path_):
                for file_ in os.listdir(path_):
                    try:
                        os.remove(os.path.join(path_, file_))
                    except:
                        continue
            else:
                try:
                    os.remove(path_)
                except:
                    continue
    sys.exit(code)
    # sys.exit(app.exec_())
