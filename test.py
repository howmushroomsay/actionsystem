from auxiliary_tools.count_main import count

import multiprocessing
import cv2
from multiprocessing import Queue
def capture(frames_queue, stop_event):
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (640, 360))
            frames_queue.put((1, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        else:
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    stop_event.set() 
    # print('hhh')

if __name__ == '__main__':
    Process_id = []
    framse_queue = Queue(100)
    re_queue = Queue(1)
    stop_event = multiprocessing.Event()
    Process_id.append(multiprocessing.Process(target=capture, args=(framse_queue, stop_event)))
    Process_id.append(multiprocessing.Process(target=count, args=(stop_event,framse_queue, re_queue)))

    for i in Process_id:
        i.start()

    re = re_queue.get()
    print(re)    
