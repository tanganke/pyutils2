#! /usr/bin/env python3
"""
Author: Anke Tang

block shuffle image

see also:
    
    - Neyshabur, Behnam, Hanie Sedghi, and Chiyuan Zhang. 2020. 
      “What Is Being Transferred in Transfer Learning?” 
      In Advances in Neural Information Processing Systems,.

"""
# %%
import torch
from torch import Tensor
import pyutils.base.log as log
from pyutils.torch import to_device
import pyutils.cppext as cppext
# %%


def get_pixel_shuffle_index(C, H, W, device=torch.device('cpu')):
    index = torch.empty((C, H * W), dtype=torch.int64)
    cppext.get_pixel_shuffle_index_i64(index.numpy())
    index = index.view(C, H, W)

    if index.device != device:
        index = index.to(device)
    return index


def pixel_shuffle(img: Tensor) -> Tensor:
    """
    per-pixel channel shuffle.

    Args:
        img (Tensor): (channel, H, W)

    Returns:
        Tensor: tensor with channel shuffled.
    """
    C, H, W = img.size()
    if C == 1:
        return img

    index = get_pixel_shuffle_index(C, H, W, img.device)

    ret = img.gather(0, index)
    return ret


def batch_pixel_shuffle(batch_img: Tensor) -> Tensor:
    N, C, H, W = batch_img.size()
    if C == 1:
        return batch_img

    ret = torch.empty_like(batch_img)
    for i in range(N):
        ret[i] = pixel_shuffle(batch_img[i])

    return ret


def get_block_shuffle_index(C, H, W, block_size, device=torch.device('cpu')):
    block_H, block_W = H // block_size, W // block_size

    block_idx = torch.randperm(block_H * block_W).view(block_H, block_W)
    block_idx = block_idx.repeat_interleave(block_size, dim=0)
    block_idx = block_idx.repeat_interleave(block_size, dim=1)
    assert block_idx.size() == torch.Size((H, W))
    block_col_idx = block_idx % block_W
    block_row_idx = block_idx.div(block_W, rounding_mode='floor')

    inblock_idx = torch.arange(block_size * block_size)
    inblock_idx = inblock_idx.view(block_size, block_size)
    inblock_idx = inblock_idx.repeat(block_H, block_W)
    inblock_row_idx = inblock_idx.div(block_size, rounding_mode='floor')
    inblock_col_idx = inblock_idx % block_size

    pixel_idx = block_row_idx * block_size * W + block_col_idx * block_size +\
        inblock_row_idx * W + inblock_col_idx
    pixel_idx = pixel_idx.view(1, H * W).repeat_interleave(C, dim=0)

    if pixel_idx.device == device:
        return pixel_idx
    else:
        return pixel_idx.to(device)


def block_shuffle(img: Tensor, block_size: int, pixel_shuffle: bool = False) -> Tensor:
    """
    block shuffle a image

    Args:
        img (Tensor): (channel, H, W)
        block_size (int): size of shuffle block.
        pixel_shuffle (bool, optional): 
            whether shuffle per-pixel channel. Defaults to `False`.

    Returns:
        Tensor: return image
    """
    C, H, W = img.size()
    assert H % block_size == W % block_size == 0
    pixel_idx = get_block_shuffle_index(C, H, W, block_size, img.device)
    ret = img.view(C, H * W).gather(1, pixel_idx).view(C, H, W)

    if pixel_shuffle:
        ret = pixel_shuffle(ret)
    return ret


def batch_block_shuffle(batch_img: Tensor, block_size: int, pixel_shuffle=False) -> Tensor:
    """

    Args:
        batch_img (Tensor): (#batch, channel, H, W)
        block_size (int): 
        pixel_shuffle (bool, optional): whether shuffle channel when `block_size` is 1. 
                                        Defaults to False.

    Returns:
        Tensor: return image batch.                        
    """
    assert batch_img.dim() == 4, \
        f'`batch_img` should be in shape as (#batch, channel, H, W), but get {batch_img.size()}'
    N, C, H, W = batch_img.size()
    batch_ret = torch.empty_like(batch_img)

    for i in range(N):
        batch_ret[i] = block_shuffle(batch_img[i], block_size, pixel_shuffle)

    return batch_ret

# %% TEST


def test():
    from PIL import Image
    import matplotlib.pyplot as plt
    from torchvision import transforms

    # load test image & show
    img = Image.open('data/airplane.jpg').convert('RGB').resize((224, 224))
    plt.imshow(img)
    plt.show()

    img_tensor = transforms.PILToTensor()(img)
    with log.TimeIt():
        img_tensor = block_shuffle(img_tensor, 224, pixel_shuffle=True)
    img = transforms.ToPILImage()(img_tensor)
    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    test()

# %%
