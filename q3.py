# Import the correct libraries/modules
import csv
import sys
import matplotlib.pyplot as plt
import os
import numpy as np


# Function that loads the census data
def loadCensus(fileLocation):

    # Create a dictionary for the result
    result = {}

    # Open using "with" as it will close the file after
    with open(fileLocation, "r", encoding="utf-8") as file:

        # Use a csv reader to read the file
        reader = csv.reader(file)
        next(reader)

        # For every row in the file
        for row in reader:

            # Set the variable to each location in the row
            location = row[0]
            remote_work_rate = float(row[1])
            commute_time = float(row[2])
            mobility_rate = float(row[3])

            # Create another dictionary inside the dictionary to hold values for each location
            result[location] = {
                "remote_work_rate": remote_work_rate,
                "commute_time": commute_time,
                "mobility_rate": mobility_rate
            }

    # Return the dictionary
    return result


# Function that loads the turnout data
def loadTurnout(fileLocation):

    # Create a dictionary for the result
    result = {}

    # Open using "with" as it will close the file after
    with open(fileLocation, "r", encoding="utf-8") as file:

        # Use a csv reader to read the file
        reader = csv.reader(file)
        next(reader)

        # For every row in the file
        for row in reader:

            # Set the variable to each province/territory in the row
            province = row[0]
            turnout_2019 = float(row[1])
            turnout_2021 = float(row[2])
            turnout_change = float(row[3])

            # Create another dictionary inside the dictionary to hold values for each province/territory
            result[province] = {
                "turnout_2019": turnout_2019,
                "turnout_2021": turnout_2021,
                "turnout_change": turnout_change
            }

    # return the dictionary
    return result


# Main function
def main():

    # Get the dictionary for the census and turnout data
    censusData = loadCensus("q3Data/censusData.csv")
    turnoutData = loadTurnout("q3Data/turnout44and43.csv")

    # Ask the user what they would like the societal factor to be
    print("\nChoose type of societal factor:")
    print("1 = Economic mobility (remote work)")
    print("2 = Geographic mobility (commute time)")
    print("3 = Social stability (mobility rate)")

    # Take the users input
    choice = input("Enter choice (1-3): ")

    # Run if, elif, and else statements to see what they chose for the factor, and set the variable and title for the graph accordingly
    if choice == "1":
        variable = "remote_work_rate"
        title = "Remote Work Rate vs Turnout Change"
    elif choice == "2":
        variable = "commute_time"
        title = "Commute Time vs Turnout Change"
    elif choice == "3":
        variable = "mobility_rate"
        title = "Mobility Rate vs Turnout Change"
    else:
        print("Invalid choice")
        return

    # Create lists for the x, and y axis, as well as the labels
    x = []
    y = []
    labels = []

    # For every location in the census data that is also in the turnout data
    for location in censusData:
        if location in turnoutData:

            # Append the info into the x and y axis and the labels lists accordingly
            x.append(censusData[location][variable])
            y.append(turnoutData[location]["turnout_change"])
            labels.append(location)

    # Convert the lists to numpy
    x_np = np.array(x)
    y_np = np.array(y)

    # Get the line of best fit by finding the slope and intercept of the line
    slope, intercept = np.polyfit(x_np, y_np, 1)

    # Create margin values to properly center the graph visually
    x_margin = (max(x_np) - min(x_np)) * 0.1 
    y_margin = (max(y_np) - min(y_np)) * 0.1

    # Create 100 evenly spaced points across the X-axis range with margin, then calculate the corresponding y values using y = mx + b 
    x_line = np.linspace(min(x_np) - x_margin, max(x_np) + x_margin, 100)
    y_line = slope * x_line + intercept

    # Initialize the plot with a specific size and a light gray background
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor('#f7f7f7')

    # Assign colors: Green for positive turnout change, Red for negative
    colors = ['#2ecc71' if yi > 0 else '#e74c3c' for yi in y]

    # Create the scatter plot with semi-transparent points and black outlines
    ax.scatter(x, y, s=80, c=colors, edgecolor='black', alpha=0.85)

    # Loop through data to label each individual point with the corresponding province/territory
    for xi, yi, loc in zip(x, y, labels):
        ax.annotate(loc, (xi, yi), textcoords="offset points", xytext=(5, 5), fontsize=9)

    # Draw the dotted blue regression line to show the line of best fit
    ax.plot(x_line, y_line, linestyle=':', linewidth=1.5, color='blue')

    # Set the main title and format the X/Y axis labels for readability
    ax.set_title(f"{title}", fontsize=16, weight='bold')
    ax.set_xlabel(variable.replace("_", " ").title(), fontsize=12)
    ax.set_ylabel("Turnout Change (2021 - 2019)", fontsize=12)

    # Add a grid and remove the top/right border lines so the graph looks cleaner
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Draw solid lines for the X and Y axes only if they are inside the data range 
    if min(y_np) < 0 < max(y_np):  
        ax.axhline(0, linewidth=1)

    if min(x_np) < 0 < max(x_np):
        ax.axvline(0, linewidth=1)

    # Set axis limits so the graph is centered properly instead of being shifted 
    ax.set_xlim(min(x_np) - x_margin, max(x_np) + x_margin)
    ax.set_ylim(min(y_np) - y_margin, max(y_np) + y_margin)

    # Adjust padding so that nothing gets cut off
    plt.tight_layout()

    # Make an output directory called "Q3 Results"
    outputDirectory = "Q3 Results"
    os.makedirs(outputDirectory, exist_ok=True)

    # Have the file for the pdf be called the correct name correspodnig to the factor the user chose
    filename = f"turnout_analysis_{variable}.pdf"
    filepath = os.path.join(outputDirectory, filename)

    # Save the pdf into that filepath
    plt.savefig(filepath, bbox_inches='tight')

    # Tell the user that the graph was successfully added to the folder and created
    print("Graph successfully generated and saved in 'Q3 Results' folder")


# To run the code
if __name__ == "__main__":
    main()