import csv
import json

csvfile = open('myData.csv', 'r')
jsonfile = open('data.json', 'w')

fieldnames = ["CountryName","EPI Rank","EPI Score","EPI Proficiency",
    "HumanDevelopmentIndexRank","HumanDevelopmentIndex","LevelofDevelopment","LifeExpectancyatBirth","ExpectedYearsOfSchooling","MeanYearsOfSchooling","GrossNationalIncome(perCapita)", "Region"]
reader = csv.DictReader(csvfile, fieldnames)

for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')

print "converted file!"