import torch
import os
import json

#Input:[tet,y]
#Label:[Shift,swa,swb]
class CSTData(torch.utils.data.Dataset):
    def __init__(self,labelFile,mean=None,std=None):
        super().__init__()
        self.label=json.load(open(labelFile))

        #Change from list to tensor if mean is provided
        if mean!=None:
            print("Normalize the data")
            mean=torch.FloatTensor(mean)
            std=torch.FloatTensor(std)

        self.mean=mean
        self.std=std
    def __getitem__(self,i):            
        data=self.label[i]

    # Change data into tensor format;
        x=[float(data["tet"]),float(data["y"])]
        x=torch.as_tensor(x,dtype=torch.float32)  

        y=[float(data["h"]),float(data["Shift"]),float(data["swA"]),float(data["swB"])]
        y=torch.as_tensor(y,dtype=torch.float32)   

        #Normalize the data if mean and std are provided
        if self.mean!=None:
            x=self.applyMeanStd(x)
        
        return x,y

    def __len__(self):
        return (len(self.label))

    def applyMeanStd(self,x):
        x=(x-self.mean)/self.std
        return x;

    
def getMeanStd(labelFile):
        data=CSTData(labelFile)
        loader = torch.utils.data.DataLoader(data, batch_size=256)
        samples,sum_x,square_x=0,0,0
        for x,y in loader:
            batch=x.size(0)
            sum_x+=torch.sum(x,dim=0)
            square_x+=torch.sum(x.pow(2),dim=0)
            #Update total samples
            samples+=batch

        #Mean=Sum/numOfSamples
        mean_x=sum_x/samples
        std_x=(square_x/samples-mean_x**2)
        std_x=torch.sqrt(std_x)

        return mean_x,std_x
   
