import csv
import sys
import matplotlib.pyplot as plt
import os


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

liberal43VoteShare = {}
liberal44VoteShare = {}
liberalVoteShareDelta = {}
cpiDelta = {}

majorCanadianParties=["Liberal","Conservative","NDP-New Democratic Party","Green Party","Bloc Québécois","People's Party"]
cpiCategories = ["FOOD","SHELTER"]

#Loading Election Data
def loadElection(fileLocation):
    resultDict = {}
    with open(fileLocation, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for index,row in enumerate(reader):
            if index == 0:
                continue
            location = row[0].split("/")[0]
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
            category = row[2].upper()
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

#Calculating voting share of a specific party 
def calculateVoteShare(voteDict,party):
    resultDict = {}
    for location in voteDict:
        totalVotes = sum(voteDict[location].values())
        resultDict[location] = (voteDict[location][party] / totalVotes)
    return resultDict

#Calculating change in voting share over multiple voting periods
def calculateVoteShareDelta(oldVoteShare,newVoteShare):
    resultDict = {}
    for location in newVoteShare:
        resultDict[location] = round((newVoteShare[location] - oldVoteShare[location]) * 100, 2)
    return resultDict

#Calculating CPI change 
def calculateCPIdelta(cpiData,date,cpiCategory): #Type is 'Food' or 'Shelter'
    resultDict = {}
    for location in cpiData:
        resultDict[location] = round((cpiData[location]["2021-09"][cpiCategory] - cpiData[location][date][cpiCategory])/cpiData[location][date][cpiCategory]  * 100,2)
    return resultDict

#Main Loop
def main():

    #Make sure all needed arguments are given
    if len(sys.argv) != 3:
        print("Usage: python q1.py <CPI Start Date> <CPI Category>")
        print("Example: python q1.py 2019-10 FOOD")
        return

    #Extract data from arguments
    date = sys.argv[1]
    category = sys.argv[2].upper()

    #Validate argument of category given
    if category not in cpiCategories:
        print("Invalid category. Choose from:", cpiCategories)
        return

    #Load CSV data
    election43 = loadElection("election43/table_tableau12.csv")
    election44 = loadElection("election44/table_tableau12.csv")
    cpiData = loadCPI("cpiData/processedCPIdata.csv")

    #Validate date given in argument
    if date not in cpiData["Ontario"]:
        print("Invalid date, use dates only from 2019-10 to 2021-09, use formatting YYYY-MM")
        return    

    #Calculate votes by party for both elections
    votesByProvince43 = calculateVotes(election43)
    votesByProvince44 = calculateVotes(election44)

    #Calculate liberal vote shares
    liberal43VoteShare = calculateVoteShare(votesByProvince43,majorCanadianParties[0])
    liberal44VoteShare = calculateVoteShare(votesByProvince44,majorCanadianParties[0])
    liberalVoteShareDelta = calculateVoteShareDelta(liberal43VoteShare,liberal44VoteShare)

    #Calculate CPI delta from argument date to 2021 election date
    cpiDelta = calculateCPIdelta(cpiData,date,category)

    #Graph information below
    x = []  # CPI change
    y = []  # Vote share change
    labels = []

    #Load X and Y data for graph
    for location in cpiDelta:
        if location in liberalVoteShareDelta:
            x.append(cpiDelta[location])
            y.append(liberalVoteShareDelta[location])
            labels.append(location)
    

    #Code to build graph
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor('#f7f7f7')

    # Color points (green = gain, red = loss)
    colors = ['#2ecc71' if yi > 0 else '#e74c3c' for yi in y]

    #Stuff to make graph look better
    ax.scatter(x, y, s=80, c=colors, edgecolor='black', alpha=0.85)
    for xi, yi, loc in zip(x, y, labels):
        ax.annotate(loc,(xi, yi),textcoords="offset points",xytext=(5,5),fontsize=9)

    #Graph labels and titles
    ax.set_title("CPI Delta vs Liberal Vote Share Change", fontsize=16, weight='bold')
    ax.set_xlabel(f"CPI % Change ({category.capitalize()})", fontsize=12)
    ax.set_ylabel("Liberal Vote Share Change (Percentage Point Change)", fontsize=12)

    #Graph stuff to make it look better
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    plt.tight_layout()

    #Output graph to PDF 
    outputDirectory = "Q1 Results"
    os.makedirs(outputDirectory, exist_ok=True)
    filename = f"cpi_vs_vote_{date}_{category}.pdf"
    filepath = os.path.join(outputDirectory, filename)
    plt.savefig(filepath, bbox_inches='tight')

    print("Data successfully processed, PDF saved to 'Q1 Results' subdirectory")


if __name__ == "__main__":
    main()