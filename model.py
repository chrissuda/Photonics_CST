import torch
from torch import nn
import torch.nn.functional as F

# Model for CST DATA
class CSTModel(nn.Module):
    def __init__(self, input_size, hidden_size_1, hidden_size_2, hidden_size_3,num_classes):
        super().__init__()
        # assign layer objects to class attributes
        self.fc1 = nn.Linear(input_size, hidden_size_1)
        nn.init.kaiming_normal_(self.fc1.weight)
        self.bn1=torch.nn.BatchNorm1d(hidden_size_1)

        self.fc2 = nn.Linear(hidden_size_1, hidden_size_2)
        nn.init.kaiming_normal_(self.fc2.weight)
        self.bn2=torch.nn.BatchNorm1d(hidden_size_2)

        # self.fc3 = nn.Linear(hidden_size_2, hidden_size_3)
        # nn.init.kaiming_normal_(self.fc3.weight)
        # self.bn3=torch.nn.BatchNorm1d(hidden_size_3)

        # self.fc4 = nn.Linear(hidden_size_3, hidden_size_3)
        # nn.init.kaiming_normal_(self.fc4.weight)
        # self.bn4=torch.nn.BatchNorm1d(hidden_size_3)

        self.fc5 = nn.Linear(hidden_size_2, hidden_size_1)
        #nn.init.kaiming_normal_(self.fc5.weight)

        self.fc6 = nn.Linear(hidden_size_1, num_classes)
        #nn.init.kaiming_normal_(self.fc6.weight)

    def forward(self, x):
        # forward always defines connectivity
        x = F.relu(self.fc1(x))
        x=self.bn1(x)

        x = F.relu(self.fc2(x))
        x=self.bn2(x)
    
        # x = F.relu(self.fc3(x))
        # #x=self.bn3(x)
        
        # x = F.relu(self.fc4(x))
        
        x = F.relu(self.fc5(x))

        score = F.relu(self.fc6(x))
        
        return score

class CSTModel2(nn.Module):
    def __init__(self, input_size, hidden_size_1,hidden_size_2,num_classes):
        super().__init__()
        # assign layer objects to class attributes
        self.fc1 = nn.Linear(1, 1)
        nn.init.kaiming_normal_(self.fc1.weight)

        self.fc7 = nn.Linear(1, 1)
        nn.init.kaiming_normal_(self.fc7.weight)
        
        self.fc2 = nn.Linear(1, 1)
        nn.init.kaiming_normal_(self.fc2.weight)

        self.fc8 = nn.Linear(1, 1)
        nn.init.kaiming_normal_(self.fc8.weight)


        self.fc3 = nn.Linear(2, hidden_size_1)
        nn.init.kaiming_normal_(self.fc3.weight)

        self.fc4 = nn.Linear(hidden_size_1, hidden_size_2)
        nn.init.kaiming_normal_(self.fc4.weight)

        self.fc5 = nn.Linear(hidden_size_2, num_classes)
        nn.init.kaiming_normal_(self.fc5.weight)

        self.fc6 = nn.Linear(num_classes, num_classes)
        nn.init.kaiming_normal_(self.fc6.weight)

    def forward(self, x):
        # forward always defines connectivity
        x1 = F.relu(self.fc1(torch.unsqueeze(x[:,0],-1)))
        x1=F.relu(self.fc7(x1))

        x2 = F.relu(self.fc2(torch.unsqueeze(x[:,1],-1)))
        x2=F.relu(self.fc8(x2))
        #Concatenate layers
        x = torch.cat((x1, x2), 1)

        x = F.relu(self.fc3(x))
        
        x = F.relu(self.fc4(x))
        
        x = F.relu(self.fc5(x))

        score = F.relu(self.fc6(x))
        
        return score



class preModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        # assign layer objects to class attributes
        self.fc1 = nn.Linear(input_size, hidden_size)
        nn.init.kaiming_normal_(self.fc1.weight)

        self.fc2 = nn.Linear(hidden_size, hidden_size)
        nn.init.kaiming_normal_(self.fc2.weight)

        self.fc3 = nn.Linear(hidden_size, num_classes)
        nn.init.kaiming_normal_(self.fc3.weight)

    def forward(self, x):
        # forward always defines connectivity
        x = torch.flatten(x)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        scores = F.relu(self.fc3(x))
        return scores


class GPN(nn.Module):
    def __init__(self, input_size_XPolar, hidden_size_XPolar, num_classes_XPolar,
                    input_size_YPolar, hidden_size_YPolar, num_classes_YPolar,
                    input_size_Properties, hidden_size_Properties, num_classes_Properties):
        super().__init__()
        # assign layer objects to class attributes

        self.Model_XPolar = preModel(
            input_size_XPolar, hidden_size_XPolar, num_classes_XPolar)
        self.Model_YPolar = preModel(
            input_size_YPolar, hidden_size_YPolar, num_classes_YPolar)
        self.Model_Properties = preModel(
            input_size_Properties, hidden_size_Properties, num_classes_Properties)

        self.fc1 = nn.Linear(input_size, hidden_size)
        nn.init.kaiming_normal_(self.fc1.weight)

        self.fc2 = nn.Linear(hidden_size, hidden_size)
        nn.init.kaiming_normal_(self.fc2.weight)

        self.fc3 = nn.Linear(hidden_size, hidden_size)
        nn.init.kaiming_normal_(self.fc3.weight)

        self.fc4 = nn.Linear(hidden_size, hidden_size)
        nn.init.kaiming_normal_(self.fc4.weight)

        self.fc5 = nn.Linear(hidden_size, hidden_size)
        nn.init.kaiming_normal_(self.fc5.weight)

        self.fc6 = nn.Linear(hidden_size, hidden_size)
        nn.init.kaiming_normal_(self.fc6.weight)

        self.fc7 = nn.Linear(hidden_size, hidden_size)
        nn.init.kaiming_normal_(self.fc7.weight)

        self.fc8 = nn.Linear(hidden_size, num_classes)
        nn.init.kaiming_normal_(self.fc8.weight)

    def forward(self, x):
        # forward always defines connectivity
        xPolar=self.Model_XPolar(x)
        yPolar=self.Model_YPolar(x)
        properties=self.Model_Properties(x)
        x=torch.cat((xPolar,yPolar,properties), 1) #concatenate along with the x-axis

        x=F.relu(self.fc1(x))
        x=F.relu(self.fc2(x))
        x=F.relu(self.fc3(x))
        x=F.relu(self.fc4(x))
        x=F.relu(self.fc5(x))
        x=F.relu(self.fc6(x))
        x=F.relu(self.fc7(x))
        scores=F.relu(self.fc8(x))

        return scores
        

class SPN(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        # assign layer objects to class attributes
        self.fc1 = nn.Linear(input_size, hidden_size)
        nn.init.kaiming_normal_(self.fc1.weight)

        self.fc2 = nn.Linear(hidden_size, hidden_size)
        nn.init.kaiming_normal_(self.fc2.weight)

        self.fc3 = nn.Linear(hidden_size, hidden_size)
        nn.init.kaiming_normal_(self.fc3.weight)

        self.fc4 = nn.Linear(hidden_size, hidden_size)
        nn.init.kaiming_normal_(self.fc4.weight)

        self.fc5 = nn.Linear(hidden_size, hidden_size)
        nn.init.kaiming_normal_(self.fc5.weight)

        self.fc6 = nn.Linear(hidden_size, hidden_size)
        nn.init.kaiming_normal_(self.fc6.weight)

        self.fc7 = nn.Linear(hidden_size, hidden_size)
        nn.init.kaiming_normal_(self.fc7.weight)

        self.fc8 = nn.Linear(hidden_size, num_classes)
        nn.init.kaiming_normal_(self.fc8.weight)

    def forward(self, x):
        # forward always defines connectivity
        x=torch.cat((x,x),0) #Create the input with 2xbatch_size
        					# One for XPolarization and one for YPolarization's sepctrum

        x=F.relu(self.fc1(x))
        x=F.relu(self.fc2(x))
        x=F.relu(self.fc3(x))
        x=F.relu(self.fc4(x))
        x=F.relu(self.fc5(x))
        x=F.relu(self.fc6(x))
        x=F.relu(self.fc7(x))
        scores=F.relu(self.fc8(x))

        return scores
