import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.distributions.categorical import Categorical


# def load_lines(path):
#   lines = []
#   with open(path, "r") as f:
#     for line in f:
#       lines.append(line.strip())
#   return lines


# def build_alphabet(lines):
#   alphabet = ""
#   for line in lines:
#     for char in line:
#       if char not in alphabet:
#         alphabet += char
#   return alphabet


# def prepare_line(alphabet, line):
#   indices = map(lambda ch: alphabet.index(ch), line)
#   tensor = torch.Tensor(indices).int()
#   return tensor


class RNN(nn.Module):
  def __init__(self, n_chars, char_size, hidden_size):
    super(RNN, self).__init__()
    self.hidden_size = hidden_size
    self.embed = nn.Embedding(n_chars, char_size)
    self.lstm = nn.LSTM(char_size, hidden_size)
    self.logits = nn.Linear(hidden_size, n_chars)

  def forward(self, inputs):
    batch_size = inputs.size(dim=1)
    hidden = (torch.zeros(1, batch_size, self.hidden_size).float(),
              torch.zeros(1, batch_size, self.hidden_size).float())
    embedded = self.embed(inputs)
    out, hidden = self.lstm(embedded, hidden)
    logits = self.logits(out)
    return logits

  def generate(self, start):
    with torch.no_grad():
      sample = torch.tensor([[start]])
      hidden = (torch.zeros(1, 1, self.hidden_size).float(),
                torch.zeros(1, 1, self.hidden_size).float())
      for i in range(80):
        embedded = self.embed(sample)
        out, hidden = self.lstm(embedded, hidden)
        logits = self.logits(out)
        dist = Categorical(logits=logits[-1].view(-1))
        nxt = dist.sample().unsqueeze(0).unsqueeze(0)
        sample = torch.cat([sample, nxt])
      return sample




# def main():
#   lines = load_lines("bundle.txt")
#   alphabet = build_alphabet(lines)

#   embed = nn.Embedding(len(alphabet), 32)
#   lstm = nn.LSTM(32, 16)
#   logit = nn.Linear(16, len(alphabet))
#   pred = nn.Softmax(1)


# if __name__ == "__main__":
#   main()
