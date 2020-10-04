import torch
from util import*
from torchData import*
from model import CSTModel
import wandb

batch_size=128
epochs=50

train_labelFile="./data/label.json"
val_labelFile="./data/label.json"
mean,std=getMeanStd(train_labelFile)

print("mean:",mean," std:",std)

#Create a dataset object
trainset=CSTData(train_labelFile)
valset=CSTData(val_labelFile)


#Create a Dataloader to load the data
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True)

valloader = torch.utils.data.DataLoader(valset, batch_size=5,
                                         shuffle=True)

#Set up the model
model=CSTModel2(2,10,50,4)
#Require parameters update in backproporgation
for param in model.parameters():
        param.requires_grad = True
        
# Using GPU or CPU
if torch.cuda.is_available():
	device = torch.device('cuda')
	torch.backends.cuda.cufft_plan_cache.clear()
else:
	device = torch.device('cpu')

#Setting up an learning optimizer
optimizer=torch.optim.Adam(model.parameters(),lr=0.0005)
#Set up a loss function
criterion = torch.nn.MSELoss()

#call the train funciton to train the model
model=train(model,optimizer,trainloader,valloader,criterion,device,isWandb=False,epochs=epochs)

print("Finish")

torch.save(model,"model.pt")
wandb.save("model.pt")