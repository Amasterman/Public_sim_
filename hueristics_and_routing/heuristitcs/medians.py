import pandas as pd

# Load the data
data = pd.read_excel("result.xlsx")

# Filter data by algorithm
data_first = data[data["alg_name"] == "transfer"]
data_greedy = data[data["alg_name"] == "greedy"]

# Compute descriptive statistics for each algorithm (excluding the 'alg_name' column)
stats_first = data_first.drop(columns=['alg_name']).describe()
stats_greedy = data_greedy.drop(columns=['alg_name']).describe()

# Add median to the descriptive statistics
stats_first.loc["median"] = data_first.drop(columns=['alg_name']).median()
stats_greedy.loc["median"] = data_greedy.drop(columns=['alg_name']).median()

# Select only relevant performance metrics
metrics = ["distance", "time", "passenger_time", "passenger_wait", "dissatisfied", "transfers", "bus_wait"]
stats_first = stats_first.loc[["mean", "median", "std", "min", "max"], metrics]
stats_greedy = stats_greedy.loc[["mean", "median", "std", "min", "max"], metrics]

# Print the descriptive statistics for each algorithm
print("Descriptive statistics for the first algorithm:")
print(stats_first)
print("\nDescriptive statistics for the greedy algorithm:")
print(stats_greedy)
