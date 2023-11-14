import numpy as np
import torch,math
import torchvision.transforms as T
from .repnet.model import RepNet

def count_fun(stop_event, frames_queue, count_queue):
    weights = './auxiliary_tools\count_main\checkpoints\pytorch_weights.pth'
    # weights = './checkpoints\pytorch_weights.pth'
    strides = [1,2,3,4,]
    crop_size = 360
    batch_size = 16
    model = RepNet()
    state_dict = torch.load(weights)
    model.load_state_dict(state_dict)
    model.eval()
    model.to('cuda')
    model(torch.zeros(1, 3, 64, 112, 112).cuda(0))
    transform = T.Compose([
        T.ToPILImage(),
        T.CenterCrop(crop_size),
        T.Resize((112, 112)),
        T.ToTensor(),
        T.Normalize(mean=0.5, std=0.5),
    ])
    frames = []
    while not stop_event.is_set():
        if frames_queue.qsize() == 0:
            continue
        flag, frame = frames_queue.get()
        if flag == 1:
            break
        frames.append(transform(frame))
        

    print('counting...')
    best_stride, best_confidence, best_period_count,  = None, None, None
    for stride in strides:
        print('stride: ', stride)
        num_batches = int(np.ceil(len(frames)/64/stride/batch_size))
        raw_period_length = None
        raw_periodicity_score = None
        with torch.no_grad():
            for batch_idx in range(num_batches):
                idxes = torch.arange(batch_idx*batch_size*64*stride, (batch_idx+1)*batch_size*64*stride, stride)
                idxes = torch.clip(idxes, 0, len(frames)-1)
                cur_frames = torch.stack(frames, dim=0)[idxes]
                
                cur_frames = cur_frames.unflatten(0, (-1,64)).movedim(1,2).to('cuda')
                batch_period_length, batch_periodicity, _ = model(cur_frames)
                if raw_period_length is None:
                    raw_period_length = batch_period_length.cpu().flatten(0,1)
                    raw_periodicity_score = batch_periodicity.cpu().flatten(0,1)
                else:
                    raw_period_length = torch.cat([raw_period_length, 
                                                   batch_period_length.cpu().flatten(0,1)], 
                                                   dim=0)
                    raw_periodicity_score = torch.cat([raw_periodicity_score, 
                                                       batch_periodicity.cpu().flatten(0,1)], 
                                                       dim=0)

        confidence, period_length, period_count, _ = model.get_counts(raw_period_length, raw_periodicity_score, stride)
        if best_confidence is None or confidence > best_confidence:
            best_confidence,  best_period_count = confidence, period_count
    print(best_period_count.cpu()[-1])
    print(len(frames))
    count_queue.put(math.ceil(best_period_count.cpu()[-1].item()))

