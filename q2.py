import csv


def running_average_change(filename):

    industry_wages = {}
    changes = []

    with open("hourlyWageData/ontWage.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            industry = row["Industry"]
            quarter = row["Quarter"]

            try:
                wage = float(row["Wage"])
            except:
                continue

            if industry not in industry_wages:
                industry_wages[industry] = []

            industry_wages[industry].append((quarter, wage))

    # calculate quarterly changes
    for industry in industry_wages:

        wages = industry_wages[industry]

        # sort quarters chronologically
        wages.sort()

        for i in range(1, len(wages)):
            change = wages[i][1] - wages[i-1][1]
            changes.append(change)

    # running average
    if len(changes) == 0:
        return 0

    return sum(changes) / len(changes)


ont_avg_change = running_average_change("ontWage.csv")
qc_avg_change = running_average_change("quebecWage.csv")




ont_turnout = None
qc_turnout = None

with open("table_tableau04 (1).csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        if "2019" not in row["Year"]:
            continue

        province = row["Province"]

        if province == "Ontario":
            ont_turnout = float(row["Voter turnout"])

        if province == "Quebec":
            qc_turnout = float(row["Voter turnout"])


print("Average Quarterly Wage Change")
print("Ontario:", round(ont_avg_change, 2))
print("Quebec:", round(qc_avg_change, 2))

print("\n2019 Voter Turnout")
print("Ontario:", ont_turnout)
print("Quebec:", qc_turnout)

print("\nComparison:")

if ont_avg_change < 0:
    print("Ontario wages decreased before the election.")
else:
    print("Ontario wages increased before the election.")

if qc_avg_change < 0:
    print("Quebec wages decreased before the election.")
else:
    print("Quebec wages increased before the election.")