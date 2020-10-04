import json
import csv
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
	#Create a list to hold dict data
	param=[]

	#Reading validation params file
	if "validation" in file:
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
		'''
		Reading training params .csv file
		@variable param
		[
		{
		"Shift":4,
		"h":0.5,
		"swA":1,
		"swB":1,
		"tet":1.22173
		}]
		'''
		with open(file,"r") as paramFile:
			lines=csv.DictReader(paramFile)
			for line in lines:
				del line["3D Run ID"]
				param.append(line)

	paramFile.close()
	return param

def readData(file):
	#Open data file
	text_file = open(file, "r")
	lines = text_file.readlines()

	#Create a list to hold data
	data=[]

	#Reading validation data file
	if "validation" in file:
		step=1004 #Only extrct the data whose frequency=10GHz

	#Reading training data file
	else:
		#Only extrct the data whose frequency=10GHz
		step=4 

	'''
	Iterate through the txt file
	Extract data if its frequency is at 10GHZ. 
	@variable data 
	[{
	"x":10,
	"y":reflectance
	},]
	'''
	for line in lines[2::step]:
		num=line.strip().split(" ")
		dataDict={"x":float(num[0]),"y":float(num[-1])}
		data.append(dataDict)

	text_file.close()
	return(data)


def storeData(newData_file,data=None,param=None,dataFile=None,paramFile=None):
	if  dataFile!=None and paramFile!=None:
		#Read parameters file
		param=readParam(paramFile)

		#Read data file
		data=readData(dataFile)

		#Check if two files are all correct
		validateDataParam(data,param)

	elif data!=None and param!=None:
		pass
	else:
		raise Exception("Must provide (data and param) or (dataFile and paramFile) argument")

	'''
	Group param and data file together 
	And store them in a single json file
	@variable label:
	[{
    "x": 10.0,
    "y": 0.00063410069,
    "Shift": "4",
    "h": "0.5",
    "swA": "1",
    "swB": "1",
    "tet": "1.22173"
  },] 
	'''

	#Group data and param file together
	label=[]
	for i in range(len(data)):
		#Merge data and param two dict together
		#and append it to label
		label.append({**data[i],**param[i]})

	#Store labels file in a .json file
	with open(newData_file,"w") as f:
		json.dump(label,f,indent=2)

	print("Label stores successfully!!!")



train_paramFile="data/result_navigator_h.csv";
train_dataFile="data/train_SZmax(6).Zmax(1)_h.txt"
train_labelFile="data/label.json"

# val_paramFile="data/validation/val_paramLogFile.txt";
# val_dataFile="data/validation/val_SZmax(6).Zmax(1).txt"
# val_labelFile="data/validation/val_label.json"

storeData(train_labelFile,dataFile=train_dataFile,paramFile=train_paramFile)
