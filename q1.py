import csv

election43 = {}
election44 = {}

#Election Data structured as following
#Location -> Candidate -> Votes

cpiData = {} 

#CPI Data Dictionary Structed as the following: 
# Location -> Date -> Category -> CPI Value

votesByProvince43 = {}
votesByProvince44 = {}

#Votes Structured as following:
#Location -> Party -> Votes

majorCanadianParties=["Liberal","Conservative","NDP-New Democratic Party","Green Party","Bloc Québécois","People's Party"]

#Loading Election Data
def loadElection(fileLocation):
    resultDict = {}
    with open(fileLocation, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for index,row in enumerate(reader):
            if index == 0:
                continue
            location = row[0]
            candidate = row[3]
            votes = int(row[6])

            if location not in resultDict:
                resultDict[location] = {}

            resultDict[location][candidate] = votes
    return resultDict
#Loading CPI Data
def loadCPI(fileLocation):
    resultDict = {}
    with open(fileLocation, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for index,row in enumerate(reader):
            if index == 0:
                continue
            date = row[0]
            location = row[1]
            category = row[2]
            value = float(row[3])

            if "," in location:
                continue
            if location not in resultDict:
                resultDict[location] = {}
            
            if date not in resultDict[location]:
                resultDict[location][date] = {}

            resultDict[location][date][category] = value
    return resultDict

#Calculate Votes by party
def calculateVotes(electionData):
    resultDict = {}
    for location in electionData:
        resultDict[location] = {}
        for candidate in electionData[location]:
            found = False
            for party in majorCanadianParties:
                if party in candidate:
                    if party not in resultDict[location]:
                        resultDict[location][party] = 0
                    resultDict[location][party] += electionData[location][candidate]
                    found = True
                    break
            if not found:
                if "smallParties" not in resultDict[location]:
                        resultDict[location]["smallParties"] = 0
                resultDict[location]["smallParties"] +=  electionData[location][candidate]
    return resultDict



election43 = loadElection("election43/table_tableau12.csv")
election44 = loadElection("election44/table_tableau12.csv")
cpiData = loadCPI("cpiData/processedCPIdata.csv")
votesByProvince43 = calculateVotes(election43)
votesByProvince44 = calculateVotes(election44)

for party in votesByProvince44:
    print(party, votesByProvince44[party],"\n")

for location in cpiData:
    print("\n",location)
    for date in cpiData[location]:
        print("        ",cpiData[location][date],"")