import csv
import httplib2
from apiclient.discovery import build
import urllib
import json
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt 

# This API key is provided by google as described in the tutorial
API_KEY = 'AIzaSyAS6ZUpFfdNszyRyBhZ8ShYnUdkGvPJTy4'

# This is the table id for the fusion table
#TABLE_ID = "1xBlXG-D3BiB2tutuoxD401BNI_ZW7KzFf1gl7xr7"
    
TABLE_ID = "1NFQyvuy7n-c9uQkIBtxg0dk7XILOMF7-YysXiygk"

try:
    fp = open("data/data.json")
    response = json.load(fp)
except IOError:
    service = build('fusiontables', 'v1', developerKey=API_KEY)
    query = "SELECT * FROM " + TABLE_ID 
    response = service.query().sql(sql=query).execute()
    fp = open("data.json", "w+")
    json.dump(response, fp)

#print response["columns"]
print response

summary = {}
fieldnames = ["CountryName","EPI Rank","EPI Score","EPI Proficiency",
    "HumanDevelopmentIndexRank","HumanDevelopmentIndex","LevelofDevelopment",
    "LifeExpectancyatBirth","ExpectedYearsOfSchooling","MeanYearsOfSchooling",
    "GrossNationalIncome(perCapita)", "Region"]

ignore = [u'HumanDevelopmentIndexRank', u'HumanDevelopmentIndex', u'LifeExpectancyatBirth',
 u'ExpectedYearsOfSchooling', u'MeanYearsOfSchooling', u'GrossNationalIncome(perCapita)', 
 u'GNIpercapitarankminusHDI rank', u'epiRank', u'epiScore', u'2014-2015 Trend', u'LevelofDevelopment']

dataEurope = []
dataMiddleEast = []

#take the json value for a query and edit it so only the values you want are returend
def specificData(i):
    datum = {}
    for key in i:
        if key not in ignore:
            datum[key] = i[key]
    return datum


def getEuropeData():
    for item in response:
        if item["Region"] == "Europe":
            newData = specificData(item)
            dataEurope.append(newData)
    return dataEurope

def getMiddleEastData():
    for item in response:
        if item["Region"] == "Middle East And North Africa":
            newData = specificData(item)
            dataMiddleEast.append(newData)
    return dataMiddleEast

def formatData(data):
    #data in json format
    #formattedData = [["EPI Proficiency", "CountryName", "Region", "EPI Score"]]
    #columns = [u'EPI Proficiency', u'CountryName', u'Region', u'EPI Score']
    formattedData = [[ "CountryName", "EPI Score"]]
    columns = [u'CountryName', u'EPI Score']
    for datum in data:
        formattedData.append(getRow(datum, columns))
    print formattedData
    return formattedData

def getRow(datum, columns):
    row = []
    for col in columns:
        if type(datum[col]) == unicode:
            row.append(str(datum[col]))
        else:row.append(datum[col])
    return row

#getEuropeData()
#formatData(dataEurope)
#getMiddleEastData()
#formatData(dataMiddleEast)
