import torch
from tqdm import tqdm
from statistics import mean
import wandb

def train(model,optimizer,trainloader,valloader,criterion,device,epochs=2):
	#Initialize wandb
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
		val_loss,val_ShiftDiff,val_swaDiff,val_swbDiff=evaluate(model,valloader,criterion)
		print("Epochs:",e," train_loss:",train_loss.data," val_loss:",val_loss,
			" ShiftDiff:",val_ShiftDiff*100,"%",
			" swaDiff:",val_swaDiff*100,"%",
			" swbDiff:",val_swbDiff*100,"%")

		#Log results to wandb
		wandb.log({
				"Epoch":e,
				"train_loss":train_loss,
				"val_loss":val_loss,
				"ShiftDiff":val_ShiftDiff,
				"swaDiff:":val_swaDiff,
				"swbDiff":val_swbDiff
				})

	return model


def evaluate(model,loader,criterion,device):
	lossList=[]
	ShiftDiffList,swaDiffList,swbDiffList=[],[],[]
	
	model = model.to(device=device)  # move the model parameters to CPU/GPU
	model.eval()

	with torch.no_grad:
		for x,y in loader:
			x=x.to(device=device) #move data to CPU/GPU
			y=y.to(device=device)

			target=model(x)
			lossList.append(criterion(target,y).item())
			ShiftDiffList.append(abs(target.data[0]-y.data[0])/y.data[0])
			swaDiffList.append(abs(target.data[1]-y.data[1])/y.data[1])
			swbDiffList.append(abs(target.data[2]-y.data[2])/y.data[2])

	loss=round(mean(lossList),4)
	ShiftDiffMean=round(mean(ShiftDiffList),4)
	swaDiffMean=round(mean(swaDiffList),4)
	swbDiffMean=round(mean(swbDiffList),4)

	return lossMean,ShiftDiffMean,swaDiffMean,swbDiffMean

