#!/usr/bin/env python

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from model import VAE
from dataset import ChordDataset


dataset = ChordDataset("../bundle.txt", 1)
loader = DataLoader(dataset, batch_size=4, shuffle=True, collate_fn=lambda x: x)

vae = VAE(len(dataset.alphabet), 16, 16)
vae.load_state_dict(torch.load("vae.model"), strict=False)


for i, batch in enumerate(loader):
  for song in batch:
    if song.size(0):
      song_enc = vae.encode(song)
      print(song.size())
      print(song_enc.size())
      song_dec, _ = vae.decode(song_enc, song.size(0))
      print(song_dec.size())
      print(dataset.decode(song_dec))
