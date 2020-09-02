import torch
import math

# Using GPU or CPU
if torch.cuda.is_available():
	device = torch.device('cuda')
	torch.backends.cuda.cufft_plan_cache.clear()
else:
	device = torch.device('cpu')

#Load the model
model=torch.load("model.pt",map_location=device)

#Ask for input
reflectance=input("Input the value for reflectance:")
reflectance=float(reflectance)

tet=input("Input the value for tet:")
tet=float(tet)
#Convert to radian if it is in degree
if tet>2:
    assert tet<90,"Tet(angle) must be smaller than 90"
    tet=tet*math.pi/180.0
print("You input:  tet(In radian):"+str(tet)," reflectance:"+str(reflectance))

#Creat a tensor that holds tet and reflectance
x=torch.tensor([tet,reflectance],dtype=torch.float32,device=device)
#Expand the dim
x=torch.unsqueeze(x,0)

#Put mode in evaluation model
model.eval()
#Get the output from model
target=model(x)

#Print out the result
h=round(target[0][0].item(),2)
Shift=round(target[0][1].item(),2)
swA=round(target[0][2].item(),2)
swB=round(target[0][3].item(),2)
print("h:",h,
        " Shift:",Shift,
        " swA:",swA,
        " swB:",swB)



