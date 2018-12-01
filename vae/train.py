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


prefix = torch.tensor([dataset.alphabet.index(' ')])


count = 0
for i in range(1000):
  for j, batch in enumerate(loader):
    print(i, j, count)
    optimizer.zero_grad()
    loss = torch.tensor(0, dtype=torch.float)
    for song in batch:
      if song.size(0) > 1:
        song_enc = vae.encode(song)

        # setup decode train
        dec_input = torch.cat([prefix, song[:-1]])
        dec_target = song
        song_dec = vae.predict(song_enc, dec_input)
        rec = F.cross_entropy(song_dec, dec_target)
        print(rec.item() / song.size(0))
        loss += rec
    loss.backward()
    optimizer.step()
    count += 1
    if count % 200 == 0:
      torch.save(vae.state_dict(), "vae.model")
