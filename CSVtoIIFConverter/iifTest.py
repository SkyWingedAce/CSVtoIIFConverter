from datetime import datetime
import os

rootLet = os.path.abspath(os.sep)

def transCreate(x,c):
    rtnList = []
    for i in range (0, len(x)):
        if i == 0:
            rtnList.append(x[i].replace('!',''))
        if i == 1: 
            rtnList.append("INVOICE")
        if i == 2:
            rtnList.append(c[4].split(" ")[0])
        if i == 3:
            rtnList.append("Truck: " + c[1])
        if i == 4: 
            rtnList.append("Accounts Receivable")
        if i == 5:
            rtnList.append(c[2])
        if i == 6:
            rtnList.append(c[6])
        if i == 7:
            rtnList.append(c[0])
    return rtnList


def splCreate(x,c):
    rtnList = []
    for i in range (0, len(x)):
        if i == 0:
            rtnList.append(x[i].replace('!',''))
        if i == 1: 
            rtnList.append("INVOICE")
        if i == 2:
            rtnList.append(c[4].split(" ")[0])
        if i == 3:
            rtnList.append(c[3])
        if i == 4: 
            rtnList.append("Sales Income")
        if i == 5:
            rtnList.append(c[2])
        if i == 6:
            temp = float(c[6])
            if temp == 0:
                rtnList.append(str(temp))
            else:
                rtnList.append(str(float(c[6]) * -1))
        if i == 7:
            rtnList.append(c[0])
        if i == 8:
            rtnList.append(c[5])
        if i == 9:
            if float(c[5]) == 0:
                rtnList.append(str(round(float(0.0),2)))
            else:
                rtnList.append(str(round(float(c[6])/float(c[5]), 2)))
                
    return rtnList


def endtransCreate(x):
    rtnList = []
    temp = x[0].replace('!', '')
    rtnList.append(temp)
    return rtnList


def fileCheck(z = "testfile",preFix = ""):
    try:
        f = open(preFix + z + ".csv", "r")
        f.close()
        return 1
    except IOError:
        print("File Not found.")
        return 0


def fileCheckiif(z = "testfile"):
    try:
        f = open(rootLet + "CSVtoIIFConverter\\IIF Folder\\" + z + ".iif", "r")
        f.close()
        return 1
    except IOError:
        print("File Not found.")
        return 0


def iifFileCreate(z = "testfile"):
    print("\nCreating new iifFile...\n")
    
    testFile = open(rootLet + "CSVtoIIFConverter\\IIF Folder\\" + filename + ".iif", "x")
    testFile.write(strBuild)
    testFile.close()

    print("New File created at " + rootLet + "CSVtoIIFConverter\\IIF Folder\\"+  filename + ".iif")


def currentDate():
    dateT = datetime.now()
    dateF = dateT.strftime("%m%d%Y")
    #print(str(dateF))
    return dateF

rootLet = os.path.abspath(os.sep)

#This is for grabbing  the current date to see if there is a file of that name avaliable
dateF = currentDate()

# this code gets us 
prefixFile = open(rootLet +"CSVtoIIFConverter\\CSVFolderLocation.txt","r")
prefix = prefixFile.readline()

#this line is for importing the subject line format list
format = open (rootLet +"CSVtoIIFConverter\\iifFormat.txt","r")
sf =""
formatListMat = []
for line in format:
    sf = line.strip('\n').strip('').split("\t")
    while '' in sf:
        sf.remove("")
    formatListMat.append(sf)

#print(*formatListMat, sep = "\n")
format.close()

print("Checking for .CSV files created today... \n \n")

# the following lines take user input for input filename should there not be a file matching todays date format
if (fileCheck(dateF,prefix) == 0):
    print("no file  found for current date... \n")
    filename = input("Please enter the File's name (the name is probably the date it was created)\n i.e. **07082020**: \n")
    checkRes = fileCheck(filename,prefix)
    while checkRes != 1:
        filename = input("Please enter the File's name (the name is probably the date it was created)\n i.e. **07082020**: \n")
else:
    print("CSV File found...\n \n")
    filename = dateF

# the following lines read in a CSV and create the subject line list
f = open(prefix + filename + ".csv", "r")
csvList = []
for line in f:
    s = line.strip('\n').split(",")
    csvList.append(s)
#print(*csvList, sep = "\n")
f.close()

## the following code is for formating the CSV to IIF based on a provided Format.txt 
#for x in csvList:

outputList = []
strBuild = ""
#this is the format at the top of the list
for i in formatListMat:
    for x in i:
        strBuild += (x) + "\t"
    strBuild += "\n"
##this is the body of the file
for i in range (1, len(csvList)):
    outputList.append(transCreate(formatListMat[0], csvList[i]))
    outputList.append(splCreate(formatListMat[1], csvList[i]))
    outputList.append(endtransCreate(formatListMat[2]))
### this creates string object in tab delemeted for using outputlist(the body of the CSV) information  
for i in outputList:
    for x in i:
        strBuild += (x) + "\t"
    strBuild += "\n"
#print(strBuild)

#checks to see if a iif file exists and if it does not it creates one
#otherwise it removes the duplicate and replaces it
if (fileCheckiif(filename) == 0):
    iifFileCreate(filename)
else:
    print("Removing duplicate file found...\n")
    os.remove(rootLet + "CSVtoIIFConverter\\IIF Folder\\" + filename + ".iif")
    iifFileCreate(filename)

    input()