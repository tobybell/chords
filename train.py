#!/usr/bin/env python

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader

from model import VAE
from dataset import ChordDataset


dataset = ChordDataset("../bundle.txt")
loader = DataLoader(dataset, batch_size=4, shuffle=True, collate_fn=lambda x: x)

vae = VAE(len(dataset.alphabet), 16, 16)
# vae.load_state_dict(torch.load("vae.model"))

optimizer = optim.RMSprop(vae.parameters())


for i in range(1000):
  for j, batch in enumerate(loader):
    print(i, j)
    optimizer.zero_grad()
    loss = torch.tensor(0, dtype=torch.float)
    for song in batch:
      if song.size(0):
        song_enc = vae.encode(song)
        _, song_dec = vae.decode(song_enc, song.size(0))
        rec = F.cross_entropy(song_dec, song)
        print(rec.item() / song.size(0))
        loss += rec
    loss.backward()
    optimizer.step()
  torch.save(vae.state_dict(), "vae.model")
