import torch
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

			#Feed the input to our model 
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
		#calling the evaluate() function
		val_loss,val_hErr,val_ShiftErr,val_swAErr,val_swBErr=evaluate(model,valloader,criterion,device)

		#Print out the performance result
		print("Epochs:",e," train_loss:",round(train_loss.item(),2)," val_loss:",val_loss,
		" hErr:%.2f ShiftErr:%.2f swAErr:%.2f swBErr:%.2f" %(val_hErr,val_ShiftErr,val_swAErr,val_swBErr))

		#Log results to wandb
		if isWandb:
			wandb.log({
					"Epoch":e,
					"train_loss":train_loss,
					"val_loss":val_loss,
					"hErr":val_hErr,
					"ShiftErr":val_ShiftErr,
					"swAErr:":val_swAErr,
					"swBErr":val_swBErr
					})

	return model


def evaluate(model,loader,criterion,device):
	#Initialize the running sum of each indicator
	loss,hErr,ShiftErr,swAErr,swBErr=0,0,0,0,0
	
	# move the model parameters to CPU/GPU
	model = model.to(device=device)

	# Put model into evaluation model
	model.eval()


	with torch.no_grad(): #Doesn't require parameter update in evaluation model
		#Iterate through the dataset
		for i,(x, y) in enumerate(loader):
			x=x.to(device=device) #move data to CPU/GPU
			y=y.to(device=device)

			'''
			Feed our input into model and get a prediction
			@var target [h,Shift,swA,swB]
			'''
			target=model(x)

			#Calculate loss by suppling a prediciton and ground-truth label
			loss+=criterion(target,y).item()

			#Calculate parameters error per batch
			hErr+=(torch.mean((torch.abs(target[:,0]-y[:,0])/y[:,0]))).item()
			ShiftErr+=(torch.mean((torch.abs(target[:,1]-y[:,1])/y[:,1]))).item()
			swAErr+=(torch.mean((torch.abs(target[:,2]-y[:,2])/y[:,2]))).item()
			swBErr+=(torch.mean((torch.abs(target[:,3]-y[:,3])/y[:,3]))).item()

	'''
	Update i
	i is 0 in the first loop, which suppose to be 1 instead. 
	So it has to be added 1 in the end.
	'''
	i+=1 

	#Divided by number of batches to get the mean value of each parameters value
	#Round it to desired precision
	loss=round(loss/i,2)
	hErr=round(hErr/i,4)
	ShiftErr=round(ShiftErr/i,4)
	swAErr=round(swAErr/i,4)
	swBErr=round(swBErr/i,4)

	#Return parameters' error
	return loss,hErr,ShiftErr,swAErr,swBErr

