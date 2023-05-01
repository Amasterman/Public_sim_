import pandas as pd

# Load the data
data = pd.read_excel("result.xlsx")

# Calculate descriptive statistics for each algorithm
stats_first = data[data["alg_name"] == "transfer"].describe()
stats_greedy = data[data["alg_name"] == "greedy"].describe()

# Calculate percentage differences for means or medians, excluding buses and passengers
percent_difference = (stats_first.loc["mean"].drop(["buses", "passengers"]) - 
                      stats_greedy.loc["mean"].drop(["buses", "passengers"])) / stats_greedy.loc["mean"].drop(["buses", "passengers"]) * 100

# Print the percentage differences
print("Percentage differences between the algorithms (first vs. greedy):")
print(percent_difference)

