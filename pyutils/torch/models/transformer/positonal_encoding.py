import math
import torch
from torch import Tensor
import torch.nn as nn


class positonal_encoding(nn.Module):
    """
    PE(pos, 2i)   = sin( pos/10000^(2i/d_model) )
    PE(pos, 2i+1) = cos( pos/10000^(2i/d_model) )

    where:
        pos : token(word)在序列(句子)中的位置。
        2i,2i+1:  token embedding(word embedding) 的索引位置。

    see also:

        - Vaswani, Ashish et al. 2017. “Attention Is All You Need.” 
          Advances in Neural Information Processing Systems 2017-Decem(Nips): 5999–6009. 
          http://arxiv.org/abs/1706.03762.
    """

    def __init__(self, *, d_model=512, max_len=5000):
        super().__init__()
        self.d_model = d_model
        self.max_len = max_len

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()  # (max_len, 1)
        # div_term[i] = (2 * max_len)^(2i/d_model)
        # 论文中的定义对应于 max_len=5000 的情况
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-(math.log(max_len * 2.0) / d_model)))

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)  # (1, max_len, d_model )
        self.register_buffer('pe', pe)

    def forward(self, x: Tensor) -> Tensor:
        """
        对x加上positional encoding.

        Args:
            x(Tensor):  ( batch_size, seq_len, d_model)

        Returns:
            Tensor: x + positonal encoding
        """
        # x:  ( batch_size, seq_len, d_model)
        # pe: ( 1,          max_len, d_model)
        x = x + self.pe[:, :x.size(1)]
        return x
