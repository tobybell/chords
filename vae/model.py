import torch
import torch.nn as nn
import torch.distributions as dist


class VAE(nn.Module):
  def __init__(self, n_chars, char_size, hidden_size):
    super().__init__()
    self.char_size = char_size
    self.hidden_size = hidden_size

    # Encoder.
    self.encode_lstm = nn.LSTM(char_size, hidden_size)
    self.encode_head = nn.Linear(hidden_size, hidden_size)

    # Decoder.
    self.decode_lstm = nn.LSTM(char_size, hidden_size)
    self.decode_head = nn.Linear(hidden_size, n_chars)

    # Both.
    self.embed = nn.Embedding(n_chars, char_size)

  def encode(self, inputs):
    hidden = (torch.zeros(1, 1, self.hidden_size).float(),
              torch.zeros(1, 1, self.hidden_size).float())
    embedded = self.embed(inputs)
    _, hidden = self.encode_lstm(embedded.unsqueeze(1), hidden)
    head = self.encode_head(hidden[0][0, 0])
    return head

  def predict(self, inputs, seq):
    length = seq.size(0)
    hidden = (inputs.view(1, 1, -1),
              torch.zeros(1, 1, self.hidden_size).float())
    embedded = self.embed(seq)
    out, hidden = self.decode_lstm(embedded.unsqueeze(1), hidden)
    logits = self.decode_head(out.view(length, -1))
    return logits

  def decode(self, inputs, length, start):
    hidden = (inputs.view(1, 1, -1),
              torch.zeros(1, 1, self.hidden_size).float())
    outputs = []
    chars = []
    curr = self.embed(start).view(1, 1, -1)
    for i in range(length):
      _, hidden = self.decode_lstm(curr, hidden)
      logits = self.decode_head(hidden[0][0, 0])
      char = logits.argmax()
      # char = dist.Categorical(logits=logits).sample()
      curr = self.embed(char).view(1, 1, -1)
      chars.append(char)
      outputs.append(logits)
    return torch.stack(chars), torch.stack(outputs)
