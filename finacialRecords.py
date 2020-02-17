#Author: Tabari Rudder-Fields 
#ID No.: 417000243
import csv
import numpy 
import datetime

fileNames = ['AAPL.csv','BARC.L.csv','BRK-B.csv','MCD.csv','TSCO.L.csv','WWE.csv','MSFT.csv','CSIOY.csv','ARW.csv','HIBB.csv','YUM.csv','WINA.csv','DRI.csv','GPC.csv','ALL.csv','AIG.csv','BAC.csv','CB.csv','DIS.csv','JACK.csv','JPM.csv','PGR.csv','UVV.csv','EA.csv']
Year_20 = '1999-11-01'
Year_10 = '2009-11-01'
stockDictionary = {}
stockKey = ['AAPL','BARC','BRK-B','MCD','TSCO.L','WWE','MSFT','CSIOY','ARW','HIBB','YUM','WINA','DRI','GPC','ALL','AIG','BAC','CB','DIS','JACK','JPM','PGR','UVV','EA']

def readFile(fileName, dateStr):
    fileList = []
    d1 =datetime.datetime.strptime(dateStr,'%Y-%m-%d').date()
    with open(fileName,'r') as file:
        csvReader = csv.reader(file)
        csvReader.next()
        for row in csvReader:
            if datetime.datetime.strptime(row[0],'%Y-%m-%d').date() > d1:
                fileList.append(row)
        file.close()
    return fileList

def createDictionary():
    for n in range(len(stockKey)):
        stockDictionary.update({stockKey[n]: readFile(fileNames[n],Year_20)})

def CalculateCorrelations(inputList,dateList,title):
    finalList = []
    finalList.append(title)
    for n in range(len(stockKey)):
        adj_close = []
        for i in range(len(stockDictionary[stockKey[n]])):
            if datetime.datetime.strptime(stockDictionary[stockKey[n]][i][0],'%Y-%m-%d').date() > datetime.datetime.strptime(dateList,'%Y-%m-%d').date():
                try:
                    adj_close.append(float(stockDictionary[stockKey[n]][i][5]))
                except:
                    adj_close.append(0)
        if len(adj_close) > len(inputList):
            adj_close = adj_close[:len(inputList)]
        elif len(adj_close) < len(inputList):
            inputList = inputList[:len(adj_close)]
        finalList.append(numpy.corrcoef(inputList,adj_close)[0,1])
    return finalList

def Calculations(dateList):
    final_list = []
    average = ['Averages']
    correlations = []
    volatility = ['Volatility']
    for n in range(len(stockKey)):
        adj_close = []
        for i in range(len(stockDictionary[stockKey[n]])):
            if datetime.datetime.strptime(stockDictionary[stockKey[n]][i][0],'%Y-%m-%d').date() > datetime.datetime.strptime(dateList,'%Y-%m-%d').date():
                try:
                    adj_close.append(float(stockDictionary[stockKey[n]][i][5]))
                except:
                    adj_close.append(0)                   
        average.append(numpy.average(adj_close)) 
        volatility.append(numpy.std(adj_close))
        correlations.append(CalculateCorrelations(adj_close,dateList,stockKey[n]))
    final_list.append(average)
    final_list.append(volatility)
    final_list.append(correlations)

    return final_list

def createCSv(title, date,):
    with open(title, 'w') as output_file:
        fakelist = list()
        fakelist = Calculations(date)
        csvWriter = csv.writer(output_file)
        csvWriter.writerow([' ','AAPL','BARC','BRK-B','MCD','TSCO.L','WWE','MSFT','CSIOY','ARW','HIBB','YUM','WINA','DRI','GPC','ALL','AIG','BAC','CB','DIS','JACK','JPM','PGR','UVV','EA'])
        csvWriter.writerow(fakelist[0])
        csvWriter.writerow(fakelist[1])
        csvWriter.writerow([])
        csvWriter.writerow([' ','AAPL','BARC','BRK-B','MCD','TSCO.L','WWE','MSFT','CSIOY','ARW','HIBB','YUM','WINA','DRI','GPC','ALL','AIG','BAC','CB','DIS','JACK','JPM','PGR','UVV','EA'])
        for i in range(len(fakelist[2])):
            csvWriter.writerow(fakelist[2][i])
        output_file.close()

createDictionary() 
createCSv('10 year calculations.csv',Year_10)
createCSv('20 year calculations.csv',Year_20)
