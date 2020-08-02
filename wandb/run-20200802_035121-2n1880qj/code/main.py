import torch
from util import*
from torchData import*
from model import CSTModel
from torchvision import transforms
import wandb

batch_size=256
epochs=50

train_labelFile="data/train/train_label.json"
val_labelFile="data/validation/val_label.json"
mean,std=getMeanStd(train_labelFile)

print("mean:",mean," std:",std)

transform=transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(mean=mean,
                         std=std)
        ])

trainset=CSTData(train_labelFile,transform)
valset=CSTData(val_labelFile,transform)

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
criterion = torch.nn.MSELoss()
model=train(model,optimizer,trainloader,valloader,criterion,device,epochs=epochs)

print("finish")
torch.save(model,"model.pt")