import math
from torch import nn

from . import layers
from .nets import EfficientGCN
from .activations import *


__activations = {
    'relu': nn.ReLU(inplace=True),
    'relu6': nn.ReLU6(inplace=True),
    'hswish': HardSwish(inplace=True),
    'swish': Swish(inplace=True),
}

def rescale_block(block_args, scale_args, scale_factor):
    channel_scaler = math.pow(scale_args[0], scale_factor)#1.2^2=1.44
    depth_scaler = math.pow(scale_args[1], scale_factor)#1.35^2 = 1.8225
    new_block_args = []
    for [channel, stride, depth] in block_args:
        channel = max(int(round(channel * channel_scaler / 16)) * 16, 16)
        depth = int(round(depth * depth_scaler))
        new_block_args.append([channel, stride, depth])
    return new_block_args
    #[[48,1,0.5],[24,1,0.5],[64,2,1],[128,2,1]]->
    #[[64,1,1],[32,1,1],[96,2,2],[192,2,2]]
def create(model_type, act_type, block_args, scale_args, **kwargs):
    kwargs.update({
        'act': __activations[act_type],
        'block_args': rescale_block(block_args, scale_args, int(model_type[-1])),
    })
    return EfficientGCN(**kwargs)
