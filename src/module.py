import torch
from torch import nn
import torch.nn.functional as F

import lightning as L


class NamesModule(L.LightningModule):
    def __init__(self, num_chars):
        super().__init__()
        self.model = nn.Sequential(
            nn.Embedding(num_chars, num_chars*3),

            nn.Linear(num_chars*3, 200),
            nn.ReLU(),

            nn.Linear(200, 200),
            nn.ReLU(),

            nn.Linear(200, num_chars),
        )

    def forward(self, batch, batch_idx):
        x, y = batch
        logits = self.model(x)
        loss = F.cross_entropy(logits, y)

        return loss

    def training_step(self, batch, batch_idx):
        loss = self.forward(batch, batch_idx)

        self.log("train_loss", loss)

        return loss

    def validation_step(self, batch, batch_idx):
        loss = self.forward(batch, batch_idx)

        self.log("val_loss", loss)

        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.SGD(self.parameters(), lr=1e-3)

        return optimizer
