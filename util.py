import torch
from tqdm import tqdm
from statistics import mean
import wandb

def train(model,optimizer,trainloader,valloader,criterion,device,isWandb=False,epochs=2):
	#Initialize wandb
	if isWandb:
		wandb.init(project="CST")

	# Using GPU or CPU
	model = model.to(device=device)  # move the model parameters to CPU/GPU
	print("Device:",device)

	for e in range(1,epochs+1):
		model.train()  # put model to training mode

		for i,(x, y) in enumerate(trainloader):
			x = x.to(device=device, dtype=torch.float32)  # move to device, e.g. GPU
			y = y.to(device=device, dtype=torch.float32) 
			target = model(x)

			#Calculate the loss with a pre-set Loss Function
			train_loss = criterion(target,y)
			
			# Zero out all of the gradients for the variables which the optimizer
			# will update.
			optimizer.zero_grad()

			# This is the backwards pass: compute the gradient of the loss with
			# respect to each  parameter of the model.
			train_loss.backward()

			# Actually update the parameters of the model using the gradients
			# computed by the backwards pass.
			optimizer.step()

		#Evaluate the model after every epoch
		val_loss,val_ShiftErr,val_swAErr,val_swBErr=evaluate(model,valloader,criterion,device)
		print("Epochs:",e," train_loss:",round(train_loss.item(),2)," val_loss:",val_loss,
			" ShiftErr:",val_ShiftErr*100,"%",
			" swAErr:",val_swAErr*100,"%",
			" swBErr:",val_swBErr*100,"%\n")

		#Log results to wandb
		if isWandb:
			wandb.log({
					"Epoch":e,
					"train_loss":train_loss,
					"val_loss":val_loss,
					"ShiftErr":val_ShiftErr,
					"swAErr:":val_swAErr,
					"swBErr":val_swBErr
					})

	return model


def evaluate(model,loader,criterion,device):
	#Calculate the running sum
	loss,ShiftErr,swAErr,swBErr=0,0,0,0
	
	# move the model parameters to CPU/GPU
	model = model.to(device=device)  
	# Put model into evaluation model
	model.eval()

	with torch.no_grad():
		for i,(x, y) in enumerate(loader):
			x=x.to(device=device) #move data to CPU/GPU
			y=y.to(device=device)

			target=model(x)

			loss+=criterion(target,y).item()
			ShiftErr+=(torch.mean((torch.abs(target[:,0]-y[:,0])/y[:,0]))).item()
			swAErr+=(torch.mean((torch.abs(target[:,1]-y[:,1])/y[:,1]))).item()
			swBErr+=(torch.mean((torch.abs(target[:,2]-y[:,2])/y[:,2]))).item()

	#Update i
	#i is 0 in the first loop, which suppose to be 1 instead.
	i+=1 

	loss=round(loss/i,2)
	ShiftErr=round(ShiftErr/i,4)
	swAErr=round(swAErr/i,4)
	swBErr=round(swBErr/i,4)

	return loss,ShiftErr,swAErr,swBErr

