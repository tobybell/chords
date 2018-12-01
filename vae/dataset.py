import torch
import torch.utils as utils


class ChordDataset(utils.data.Dataset):
  def __init__(self, csv_path, n_lines=None):
    self.songs = []
    self.alphabet = []
    self.vectors = []
    self.load_text(csv_path, n_lines)
    self.build_alphabet()
    self.build_vectors()

  def load_text(self, csv_path, n_lines):
    print("Loading dataset...")
    with open(csv_path, "r") as f:
      if n_lines:
        i = 0
        for line in f:
          self.songs.append(" ".join(line[:-1].split(",")))
          i += 1
          if i == n_lines:
            break
      else:
        for line in f:
          self.songs.append(" ".join(line[:-1].split(",")))

  def build_alphabet(self):
    print("Building alphabet...")
    for song in self.songs:
      for ch in song:
        if ch not in self.alphabet:
          self.alphabet += ch

  def build_vectors(self):
    print("Building vectors...")
    for song in self.songs:
      self.vectors.append(torch.tensor(list(map(self.alphabet.index, song))))

  def __len__(self):
    return len(self.songs)

  def __getitem__(self, i):
    return self.vectors[i]

  def decode(self, seq):
    return "".join(list(map(lambda i: self.alphabet[i], seq)))
