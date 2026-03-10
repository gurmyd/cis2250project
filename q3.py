import csv

# Load immigration data
immigration_data = {}

with open("immigrationCensusData/censusData.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        province = row["province"]
        immigration_data[province] = {
            "total": float(row["total_population"]),
            "new": float(row["new_immigrants"]),
            "established": float(row["established_immigrants"]),
            "non": float(row["non_immigrants"])
        }

# Load turnout data
turnout_data = {}

with open("immigrationCensusData/turnout44and43.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        province = row["province"]
        turnout_data[province] = {
            "2019": float(row["turnout_2019"]),
            "2021": float(row["turnout_2021"]),
            "change": float(row["turnout_change"])
        }

# Ask how many provinces to compare
while True:
    num = int(input("How many provinces or territories would you like to compare? (2-13): "))
    if 2 <= num <= 13:
        break
    print("Please enter a number between 2 and 13.")

# Ask immigration category
print("\nChoose immigration status to analyze:")
print("1 - New immigrants")
print("2 - Established immigrants")
print("3 - Non-immigrants")

choice = input("Enter 1, 2, or 3: ")

if choice == "1":
    category = "new"
    label = "New Immigrants"
elif choice == "2":
    category = "established"
    label = "Established Immigrants"
elif choice == "3":
    category = "non"
    label = "Non-Immigrants"
else:
    print("Invalid choice.")
    exit()

print("\nEnter the provinces/territories you want to compare:")

selected = []

for i in range(num):
    province = input(f"Province/Territory {i+1}: ")

    if province not in immigration_data or province not in turnout_data:
        print("Province not found in dataset.")
        exit()

    selected.append(province)

print("\n--- Analysis Results ---\n")

for province in selected:

    total_pop = immigration_data[province]["total"]
    imm_value = immigration_data[province][category]

    immigration_percent = (imm_value / total_pop) * 100

    turnout2019 = turnout_data[province]["2019"]
    turnout2021 = turnout_data[province]["2021"]
    change = turnout_data[province]["change"]

    print(f"{province}")
    print(f"{label} Percentage: {immigration_percent:.2f}%")
    print(f"Turnout 2019: {turnout2019}%")
    print(f"Turnout 2021: {turnout2021}%")
    print(f"Turnout Change (2019 → 2021): {change}%")
    print("\n-----------------------------\n")