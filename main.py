import torch
from util import*
from torchData import*
from model import CSTModel
import wandb

batch_size=256
epochs=50

train_labelFile="./data/label.json"
val_labelFile="./data/label.json"
mean,std=getMeanStd(train_labelFile)

print("mean:",mean," std:",std)

trainset=CSTData(train_labelFile,mean=mean,std=std)
valset=CSTData(val_labelFile,mean=mean,std=std)

trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True)
valloader = torch.utils.data.DataLoader(valset, batch_size=batch_size,
                                         shuffle=False)

#Set up the model
model=CSTModel(2,10,50,50,4)
for param in model.parameters():
        param.requires_grad = True
        
# Using GPU or CPU
if torch.cuda.is_available():
	device = torch.device('cuda')
	torch.backends.cuda.cufft_plan_cache.clear()
else:
	device = torch.device('cpu')

optimizer=torch.optim.Adam(model.parameters())
criterion = torch.nn.MSELoss()
model=train(model,optimizer,trainloader,valloader,criterion,device,isWandb=True,epochs=epochs)

print("Finish")
torch.save(model,"model.pt")
wandb.save("model.pt")