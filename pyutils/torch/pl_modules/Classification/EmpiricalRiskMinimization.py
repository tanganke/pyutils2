"""
empirical risk minimization
"""
import os
import torch
from torch import Tensor
import torch.nn as nn
import torch.nn.functional as F
import torchmetrics
import pytorch_lightning as pl
from typing import Callable

from pyutils.base import log


class EmpiricalRiskMinimization(pl.LightningModule):
    def __init__(self, net: nn.Module):
        super().__init__()

        self._net = net

        self.train_acc = torchmetrics.Accuracy()
        self.val_acc = torchmetrics.Accuracy()
        self.test_acc = torchmetrics.Accuracy()

    def forward(self, x: Tensor) -> Tensor:
        """
        Returns:
            Tensor: logits
        """
        logits = self._net(x)
        return logits

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits: Tensor = self(x)
        loss = F.cross_entropy(logits, y)
        # compute accuracy
        pred = logits.softmax(-1)
        self.train_acc(pred, y)

        self.log("Train/Loss", loss)
        self.log('Train/Accuracy', self.train_acc)

        return {'loss': loss, 'logits': logits, 'pred': pred}

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        pred = logits.softmax(-1)

        self.val_acc(pred, y)
        self.log('Validation/Accuracy', self.val_acc)

    def test_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        pred = logits.softmax(-1)

        self.test_acc(pred, y)
        self.log('Test/Accuracy', self.test_acc)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3, weight_decay=1e-4)
        return optimizer
