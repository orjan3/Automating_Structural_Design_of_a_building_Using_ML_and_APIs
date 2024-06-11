import torch
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from sklearn.datasets import load_diabetes
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter
import os
from datetime import datetime

# Crear un directorio para guardar los registros
log_dir = "logs/" + datetime.now().strftime("%Y%m%d-%H%M%S")
os.makedirs(log_dir)

# Inicializar SummaryWriter para escribir los registros en el directorio creado
writer = SummaryWriter(log_dir=log_dir)

class DiabetesDataset(Dataset):
    def __init__(self):
        super().__init__()
        self.X, self.y = load_diabetes(return_X_y=True)

    def __getitem__(self, idx):
        return (torch.tensor(self.X[idx]).float(), torch.tensor(self.y[idx]).float())
    
    def __len__(self):
        return len(self.X)  

dataset = DiabetesDataset()

train_loader = DataLoader(dataset, shuffle=True, batch_size=4)

examples = next(iter(train_loader))
features, labels = examples
print(features)
print(labels)

class LinearRegression(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_layer = torch.nn.Linear(10, 1)

    def forward(self, features):
        return self.linear_layer(features)
    
model = LinearRegression()

def train(model, epochs=10):
    optimizer = torch.optim.SGD(model.parameters(), lr=0.001)
    for epoch in range(epochs):
        for batch_idx, batch in enumerate(train_loader):
            features, labels = batch
            predictions = model(features)
            loss = F.mse_loss(predictions, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # Escribir la pérdida en los registros
            global_step = epoch * len(train_loader) + batch_idx
            writer.add_scalar("Loss", loss.item(), global_step=global_step)
            print(loss.item())

train(model)
