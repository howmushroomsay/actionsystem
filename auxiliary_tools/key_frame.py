import cv2
import numpy as np
from scipy.signal import argrelextrema

def smooth(x, window_len=30, window='hanning'):
    s = np.r_[2 * x[0] - x[window_len:1:-1],
            x, 2 * x[-1] - x[-1:-window_len:-1]]
    if window == 'flat':  # moving average平移
        w = np.ones(window_len, 'd')
    else:
        w = getattr(np, window)(window_len)
    y = np.convolve(w / w.sum(), s, mode='same')
    return y[window_len - 1:-window_len + 1]

def get_keyFrame(videopath):
    cap = cv2.VideoCapture(videopath)
    diffs = []
    pre_frame = None
    success, frame = cap.read()

    while(success):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
        if frame is not None and pre_frame is not None:
            diff = np.sum(cv2.absdiff(frame, pre_frame)) / (frame.shape[0] * frame.shape[1])
            diffs.append(diff)
        pre_frame = frame
        success, frame = cap.read()
    cap.release()
    
    diffs = smooth(np.array(diffs)) * -1
    frame_index = set(argrelextrema(diffs, np.greater)[0])
    return frame_index
print(pow(2, 10))