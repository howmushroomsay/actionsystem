"""Run the RepNet model on a given video."""
import os
import cv2
import argparse
import torch
import torchvision.transforms as T
import numpy as np
from repnet.model import RepNet
import time


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_VISUALIZATIONS_DIR = os.path.join(PROJECT_ROOT, 'visualizations')

# Script arguments
parser = argparse.ArgumentParser(description='Run the RepNet model on a given video.')
parser.add_argument('--weights', type=str, default=os.path.join(PROJECT_ROOT, 'checkpoints', 'pytorch_weights.pth'), help='Path to the model weights (default: %(default)s).')
parser.add_argument('--video', type=str, default='1.mp4', help='Video to test the model on, either a YouTube/http/local path (default: %(default)s).')
parser.add_argument('--strides', nargs='+', type=int, default=[1, 2, 3, 4,], help='Temporal strides to try when testing on the sample video (default: %(default)s).')
parser.add_argument('--device', type=str, default='cuda', help='Device to use for inference (default: %(default)s).')

if __name__ == '__main__':
    args = parser.parse_args()

    # Download the video sample if needed
    # print(f'Downloading {args.video}...')
    t =time.time()
    # Load model
    model = RepNet()
    state_dict = torch.load(args.weights)
    model.load_state_dict(state_dict)
    model.eval()
    model.to(args.device)
    transform = T.Compose([
        T.ToPILImage(),
        T.CenterCrop((1080,1080)),
        T.Resize((112, 112)),
        T.ToTensor(),
        T.Normalize(mean=0.5, std=0.5),
    ])
    frames = torch.zeros(1, 3, 64, 112, 112).cuda(0)
    model(frames)
    for video_ in os.listdir('./videos/'):
        t1 = time.time()
        video_path = os.path.join('./videos/', video_)
    
        # Read frames and apply preprocessing
        cap = cv2.VideoCapture(video_path)
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break
            frame = transform(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            frames.append(frame)
        cap.release()
        t2 = time.time()
        # Test multiple strides and pick the best one
        best_stride, best_confidence, best_period_count,  = None, None, None
        batch_size = 16
        for stride in args.strides:
            # Apply stride
            num_batches = int(np.ceil(len(frames)/64/stride/batch_size))
            raw_period_length = None
            raw_periodicity_score = None
            with torch.no_grad():
                for batch_idx in range(num_batches):
                    idxes = torch.arange(batch_idx*batch_size*64*stride, (batch_idx+1)*batch_size*64*stride, stride)
                    idxes = torch.clip(idxes, 0, len(frames)-1)
                    cur_frames = torch.stack(frames, dim=0)[idxes]
                    
                    cur_frames = cur_frames.unflatten(0, (-1,64)).movedim(1,2).to(args.device)
                    batch_period_length, batch_periodicity, _ = model(cur_frames)
                    if raw_period_length is None:
                        raw_period_length = batch_period_length.cpu().flatten(0,1)
                        raw_periodicity_score = batch_periodicity.cpu().flatten(0,1)
                    else:
                        raw_period_length = torch.cat([raw_period_length, batch_period_length.cpu().flatten(0,1)], dim=0)
                        raw_periodicity_score = torch.cat([raw_periodicity_score, batch_periodicity.cpu().flatten(0,1)], dim=0)

            confidence, period_length, period_count, _ = model.get_counts(raw_period_length, raw_periodicity_score, stride)
            if best_confidence is None or confidence > best_confidence:
                best_stride, best_confidence,  best_period_count = stride, confidence, period_count
        t3 = time.time()
        print(video_path, 'count: ', best_period_count[-1].cpu().data)
        print('load_time: ',t1-t, 'data_time: ', t2-t1, "pro_time: ", t3-t2)
        print('{:.2f}+{:.2f}+{:.2f}'.format(t1-t, t2-t1, t3-t2))
