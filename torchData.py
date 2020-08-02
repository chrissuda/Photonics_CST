import torch
import os
import json

#Input:[tet,y]
#Label:[Shift,swa,swb]
class CSTData(torch.utils.data.Dataset):
    def __init__(self,labelFile):
        super().__init__()
        self.label=json.load(open(labelFile))

    def __getitem__(self,idx):            
        data=self.label[idx]

    # Change data into tensor format;
        x=[data["tet"],data["y"]]
        x=torch.as_tensor(x,dtype=torch.float32)  

        y=[data["Shift"],data["swa"],data["swb"]]
        y=torch.as_tensor(y,dtype=torch.float32)   

        return x,y

    def __len__(self):
        return (len(self.label))
    