import json

def validateDataParam(data,param):
	#See if all the data's frequency are at 10GHz
	for i in range(len(data)):
		if data[i]["x"]!=10.0:
			raise ValueError("The:"+str(i)+"th of data: frequency is not equal to 10")

	#See if the number of dataList is equal to paramList
	if len(data)!=len(param):
		print("Data:",len(data)," Param:",len(param))
		raise ValueError("the number of data is not the same as the number of experiment(paramster)")

	print("Total Label:",len(data))
	print("Data and Param Validation Test pass!!!")

def readParam(file):
	byteOfTet=len("tet")
	byteOfShift=len("Shift")
	byteOfSwA=len("swA")
	byteOfSwB=len("swB")
	param=[]

	text_file = open(file, "r")
	lines = text_file.readlines()
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

	text_file.close()
	return param

def readData(file):
	data=[]
	step=1004 #Only extrct the data whose frequency=10GHz

	text_file = open(file, "r")
	lines = text_file.readlines()
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



train_paramFile="data/train/train_paramLogFile.txt";
train_dataFile="data/train/train_SZmax(6).Zmax(1).txt"
train_labelFile="data/train/train_label.json"

val_paramFile="data/validation/val_paramLogFile.txt";
val_dataFile="data/validation/val_SZmax(6).Zmax(1).txt"
val_labelFile="data/validation/val_label.json"

storeData(train_labelFile,dataFile=train_dataFile,paramFile=train_paramFile)
storeData(val_labelFile,dataFile=val_dataFile,paramFile=val_paramFile)