import torch
from torchData import CSTData
from model import CSTModel
import wandb

batch_size=64

train_labelFile="data/train/train_label.json"
val_labelFile="data/validation/val_label.json"

trainset=CSTData(train_labelFile)
valset=CSTData(val_labelFile)

trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True)
valloader = torch.utils.data.DataLoader(valset, batch_size=batch_size,
                                         shuffle=False)

#Set up the model
model=CSTModel(2,10,100,10,3)
for param in model.parameters():
        param.requires_grad = True
        
# Using GPU or CPU
	if torch.cuda.is_available():
		device = torch.device('cuda')
		torch.backends.cuda.cufft_plan_cache.clear()
	else:
		device = torch.device('cpu')

optimizer=torch.optim.Adam(model.parameters())
criterion = nn.MSELoss()
model=train(model,optimizer,trainloader,valloader,criterion,device,epochs=2)

print("finish")