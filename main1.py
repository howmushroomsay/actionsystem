import os
import sys

from PyQt5.QtWidgets import QApplication
from widgets import *
from auxiliary_tools import DatabaseOperation
import multiprocessing
if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)

    student_id = int(sys.argv[1])
    course_id = int(sys.argv[2])
    window_type = int(sys.argv[3])

    db = DatabaseOperation()

    if window_type == 0:
        win = Reaction_Train_Main(None, db=db, course_id=course_id, student_id=student_id)
    elif window_type == 1:
        win = Action_Follow_Main(None, db=db, action_id=course_id)
    elif window_type == 2:
        win = Action_Eval_Main(None, db=db, action_id=course_id, student_id=student_id)
    
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