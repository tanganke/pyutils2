import os
import sys
import re
import time
import subprocess
import numpy as np
import torch

from ..base import log

__all__ = ['device', 'auto_select_gpu']


def device(index: int) -> torch.device:
    """
    选择Torch硬件设备

    Args:
        ``index``: 硬件设备索引. ``index``<0 表示使用 CPU, ``index``>=0 表示使用第``index``个 GPU

    Return:
        ``device``: Torch硬件设备
    """
    # choose Torch device
    if index < 0:
        device = torch.device("cpu")
    else:
        if torch.cuda.is_available():
            device = torch.device(index)
        else:
            log.warn('CUDA is not available, use cpu instead.')
            device = torch.device("cpu")

    log.info('choose Torch device: type %s, index %s' %
             (device.type, device.index))

    return device


def auto_select_gpu(mem_bound=500, utility_bound=0, gpus=(0, 1, 2, 3, 4, 5, 6, 7), num_gpu=1, selected_gpus=None):
    """
    Example:

        >>> selected_gpus = auto_select_gpu(num_gpu=2)

    """
    if 'CUDA_VISIBLE_DEVCIES' in os.environ:
        sys.exit(0)
    if selected_gpus is None:
        mem_trace = []
        utility_trace = []
        for i in range(5):  # sample 5 times
            info = subprocess.check_output('nvidia-smi', shell=True).decode('utf-8')
            mem = [int(s[:-5]) for s in re.compile('\d+MiB\s/').findall(info)]
            utility = [int(re.compile('\d+').findall(s)[0]) for s in re.compile('\d+%\s+Default').findall(info)]
            mem_trace.append(mem)
            utility_trace.append(utility)
            time.sleep(0.1)
        mem = np.mean(mem_trace, axis=0)
        utility = np.mean(utility_trace, axis=0)
        assert(len(mem) == len(utility))
        nGPU = len(utility)
        ideal_gpus = [i for i in range(nGPU) if mem[i] <= mem_bound and utility[i] <= utility_bound and i in gpus]

        if len(ideal_gpus) < num_gpu:
            print("No sufficient resource, available: {}, require {} gpu".format(ideal_gpus, num_gpu))
            sys.exit(0)
        else:
            selected_gpus = ideal_gpus[:num_gpu]
    elif isinstance(selected_gpus, str):
        selected_gpus = selected_gpus.split(',')

    print("Setting GPU: {}".format(selected_gpus))
    os.environ['CUDA_VISIBLE_DEVICES'] = ','.join(list(map(str, selected_gpus)))
    return selected_gpus
