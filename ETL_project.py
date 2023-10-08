import glob
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime


def extractCSV():
    dataframes = []
    csvfiles = glob.glob("source/*.csv")
    for csv in csvfiles:
        df = pd.read_csv(csv)
        dataframes.append(df)

    return dataframes

def extractJSON():
    dataframes=[]
    jsonfiles = glob.glob("source/*.json")

    for json in jsonfiles:
        jf = pd.read_json(json, lines=True)
        dataframes.append(jf)

    return dataframes

def extractXML():
    dataframes=[]
    xmlfiles=glob.glob("source/*.xml")
    for xml in xmlfiles:
        tree=ET.parse(xml)
        root=tree.getroot()
        for person in root:
            name = person.find("name").text
            height = person.find("height").text
            weight = person.find("weight").text
            xm = pd.DataFrame(columns=["name", "height", "weight"], data=[[name, height, weight]])
            dataframes.append(xm)

    return dataframes

def concatData(concatData):
   return pd.concat(concatData,ignore_index=True)


def convert_and_round(value, conversion_factor):
    try:
        return round(float(value) * conversion_factor, 2)
    except ValueError:
        return None

def transformData(combinedData):

    combinedData["height"] = combinedData["height"].apply(convert_and_round, conversion_factor=0.0254)
    combinedData["weight"] = combinedData["weight"].apply(convert_and_round, conversion_factor=0.45359237)

    return combinedData

def loadData(targetFile,fromattedData):
    fromattedData.to_csv(targetFile,index=False)


def logmessage(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open("source/logfile.txt","a") as log:
        log.write(timestamp+": "+message+"\n")


if __name__ == "__main__":
    logmessage("Extraction Started")
    csvData=extractCSV()
    jsonData=extractJSON()
    xmlData=extractXML()
    allData=csvData+jsonData+xmlData
    combinedData=concatData(allData)
    logmessage("Extraction Finished")

    print(combinedData.head())

    logmessage("Started Transformation")
    formattedData=transformData(combinedData)
    print(formattedData)
    logmessage("Ended Transformation")

    logmessage("Started Loading")
    loadData("source/exractedData.csv",formattedData)
    logmessage("Finished Loading")














