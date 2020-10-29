import torch
import pandas as pd
from transformers import BertTokenizer, BertModel
import io
import os
from sklearn.metrics import classification_report, confusion_matrix

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')



def embs(df, folder):
  def chunk(lst):
      for i in range(0, len(lst), 510):
          yield [101] + lst[i:i + 510] + [102]
  tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
  model = BertModel.from_pretrained('bert-base-uncased')
  x_train = []
  for idx, text in enumerate(df['text']):
    print(idx)
    input = list(chunk(tokenizer.encode(text, add_special_tokens=False)))
    output = torch.zeros(1,512,768)
    for num, inp in enumerate(input):
      inp_id = torch.tensor(inp).unsqueeze(0)
      outputs = model(inp_id)
      output = (output + torch.cat((outputs[0], torch.zeros(1, 512-outputs[0].shape[1], 768)), 1)) / 2
    output = output.mean(1).view(-1)
    torch.save(output, f'{folder}/{idx}.pt')
    buffer = io.BytesIO()
    torch.save(output, buffer)
  print('finished')


df = pd.read_csv('train.csv')
embs(df, 'train')

df2 = pd.read_csv('test.csv')
embs(df2, 'test')


class Feedforward(torch.nn.Module):
        def __init__(self, input_size, hidden_size):
            super(Feedforward, self).__init__()
            self.input_size = input_size
            self.hidden_size  = hidden_size
            self.fc1 = torch.nn.Linear(self.input_size, self.hidden_size)
            self.relu = torch.nn.ReLU()
            self.fc2 = torch.nn.Linear(self.hidden_size, 6)
            self.sigmoid = torch.nn.Sigmoid()
        def forward(self, x):
            hidden = self.fc1(x)
            relu = self.relu(hidden)
            output = self.fc2(relu)
            output = self.sigmoid(output)
            return output


fmodel = Feedforward(input_size=1*768, hidden_size=100).cuda()
criterion = torch.nn.BCELoss()
optimizer = torch.optim.SGD(fmodel.parameters(), lr = 0.01)


labels = {'A1': torch.tensor([1,0,0,0,0,0], dtype=torch.float32, device=device),
          'A2': torch.tensor([0,1,0,0,0,0], dtype=torch.float32, device=device),
          'B1': torch.tensor([0,0,1,0,0,0], dtype=torch.float32, device=device),
          'B2': torch.tensor([0,0,0,1,0,0], dtype=torch.float32, device=device),
          'C1': torch.tensor([0,0,0,0,1,0], dtype=torch.float32, device=device),
          'C2': torch.tensor([0,0,0,0,0,1], dtype=torch.float32, device=device)
          }


fmodel.train()
epoch = 5
for epoch in range(epoch):
    
    for file in os.listdir('train'):
      if file.endswith('pt'): 
        optimizer.zero_grad()
        with open('train/'+file, 'rb') as f:
          buffer = io.BytesIO(f.read())
          x_train = torch.load(buffer)
          y_pred = fmodel(x_train.to(device))
          num = file[:-3]
          loss = criterion(y_pred.squeeze(), labels[df['level'][int(num)]])
          print('Epoch {}: line: {} train loss: {}'.format(epoch, num, loss.item()))
          loss.backward()
          optimizer.step()


fmodel.eval()
tests = []
for file in os.listdir('test/'):
      if file.endswith('pt'): 
        optimizer.zero_grad()
        with open('train/'+file, 'rb') as f:
          buffer = io.BytesIO(f.read())
          x_train = torch.load(buffer)
          y_pred = fmodel(x_train.to(device))
          tests.append(y_pred)

lv = {0: 'A1',
      1: 'A2',
      2: 'B1',
      3: 'B2',
      4: 'C1',
      5: 'C2'}
y_true = []
y_pred = []
for num, line in enumerate(tests):
  y_pred.append(lv[int(torch.max(line, 0)[1])])
  y_true.append(df2['level'][num])

print(classification_report(y_true, y_pred))
