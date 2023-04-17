import pandas as pd
from scipy.stats import ttest_rel

# Load the data into a pandas DataFrame
df = pd.read_excel("result.xlsx")

# Subset the data to include only rows with the same number of buses and passengers
subset_df = df[(df["alg_name"]=="algorithm1") & (df["alg_name"]=="algorithm2") & ((df["buses"]==df["buses"].shift()) & (df["passengers"]==df["passengers"].shift()))]

# Calculate the difference in time between the two algorithms
time_diff = subset_df[subset_df["alg_name"]=="new_heuristic"]["time"].reset_index(drop=True) - subset_df[subset_df["alg_name"]=="greedy"]["time"].reset_index(drop=True)

# Perform the paired t-test
t_statistic, p_value = ttest_rel(subset_df[subset_df["alg_name"]=="greedy"]["time"], subset_df[subset_df["alg_name"]=="new_heuristic"]["time"])

# Print the results
print("Paired t-test results:")
print("t-statistic:", t_statistic)
print("p-value:", p_value)