import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.utils.rnn import pack_sequence
from torch.utils.data import DataLoader

from lstm import RNN
from dataset import ChordDataset


dataset = ChordDataset("../bundle.txt")
print(len(dataset))
loader = DataLoader(dataset, batch_size=4, shuffle=True, collate_fn=lambda x: x)

rnn = RNN(len(dataset.alphabet), 24, 24)
rnn.load_state_dict(torch.load("trained.model"))

optimizer = optim.RMSprop(rnn.parameters())
loss_fn = nn.CrossEntropyLoss()

for i in range(1000):
  print("epoch " + str(i) + "...")
  for j, batch in enumerate(loader):
    optimizer.zero_grad()

    loss = torch.tensor(0, dtype=torch.float)

    for sample in batch:
      inputs = sample[:-1]
      labels = sample[1:]
      if inputs.size(0):
        preds = rnn(inputs.unsqueeze(1)).squeeze(1)
        loss += loss_fn(preds, labels)

    print(j, loss.item())

    loss.backward()
    optimizer.step()

  torch.save(rnn.state_dict(), "trained.model")
  print(dataset.decode(rnn.generate(0)))
