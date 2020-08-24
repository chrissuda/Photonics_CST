import json
import csv
def validateDataParam(data,param):
	#See if the number of dataList is equal to paramList
	if len(data)!=len(param):
		print("Data:",len(data)," Param:",len(param))
		raise ValueError("the number of data is not the same as the number of experiment(paramster)")

	print("Total Label:",len(data))
	print("Data and Param Validation Test pass!!!")

def readParam(file):
	#Create a list to hold dict data
	param=[]

	#Reading training params file
	if "train" in file: 
		with open(file,"r") as paramFile:
			lines=csv.DictReader(paramFile)
			for line in lines:
				del line["3D Run ID"]
				param.append(line)
		
	#Reading validation params file
	elif "validation" in file:
		byteOfTet=len("tet")
		byteOfShift=len("Shift")
		byteOfSwA=len("swA")
		byteOfSwB=len("swB")

		paramFile = open(file, "r")
		lines = paramFile.readlines()
		for line in lines:
			if line.find("tet")!=-1:
				param.append({"tet":float(line[byteOfTet+3:])})
			elif line.find("Shift")!=-1:
				param[-1]["Shift"]=float(line[byteOfShift+3:])
			elif line.find("swA")!=-1:
				param[-1]["swA"]=float(line[byteOfSwA+3:])
			elif line.find("swB")!=-1:
				param[-1]["swB"]=float(line[byteOfSwB+3:])
			else:
				pass

	else:
		raise ValueError("File name must contain train or validation")

	paramFile.close()
	return param

def readData(file):
	#Open data file
	text_file = open(file, "r")
	lines = text_file.readlines()

	#Create a list to hold data
	data=[]

	#Reading train data file
	if "train" in file:
		step=4

	#Reading validation data file
	elif "validation" in file:
		step=1004 #Only extrct the data whose frequency=10GHz

	else:
		raise ValueError("File name must contain train or validation")

	for line in lines[2::step]:
		num=line.strip().split(" ")
		dataDict={"x":float(num[0]),"y":float(num[-1])}
		data.append(dataDict)

	text_file.close()
	return(data)


#Input:[tet,y]
#Label:[Shift,swa,swb]
def storeData(newData_file,data=None,param=None,dataFile=None,paramFile=None):
	if  dataFile!=None and paramFile!=None:
		param=readParam(paramFile)
		data=readData(dataFile)
		validateDataParam(data,param)
	elif data!=None and param!=None:
		pass
	else:
		raise Exception("Must provide (data and param) or (dataFile and paramFile) argument")

	label=[]
	for i in range(len(data)):
		label.append({**data[i],**param[i]})

	with open(newData_file,"w") as f:
		json.dump(label,f,indent=2)

	print("Label stores successfully!!!")



train_paramFile="data/train/train_result_navigator.csv";
train_dataFile="data/train/train_SZmax(6).Zmax(1)_total.txt"
train_labelFile="data/train/train_label.json"

val_paramFile="data/validation/val_paramLogFile.txt";
val_dataFile="data/validation/val_SZmax(6).Zmax(1).txt"
val_labelFile="data/validation/val_label.json"

storeData(train_labelFile,dataFile=train_dataFile,paramFile=train_paramFile)
storeData(val_labelFile,dataFile=val_dataFile,paramFile=val_paramFile)
