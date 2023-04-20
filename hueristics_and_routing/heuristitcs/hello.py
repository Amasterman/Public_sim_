import pandas as pd
import numpy as np

# Load the data into a pandas DataFrame
df = pd.read_excel("result.xlsx")

# Subset the data to include only rows with the same number of buses and passengers
grouped_df = df.groupby(['buses', 'passengers']).filter(lambda x: len(x) == 2)
grouped_df = grouped_df.sort_values(['buses', 'passengers'])
print(grouped_df)

# Define a function to calculate the test statistic
def test_statistic(data):
    return np.mean(data[data['alg_name'] == 'greedy']['distance']) - np.mean(data[data['alg_name'] == 'new_heuristic']['distance'])

# Generate bootstrap samples and calculate the test statistic for each
n_bootstraps = 3000
bootstrap_stats = []
for i in range(n_bootstraps):
    bootstrap_sample = grouped_df.sample(frac=1, replace=True)
    bootstrap_stat = test_statistic(bootstrap_sample)
    bootstrap_stats.append(bootstrap_stat)

# Calculate the p-value
observed_stat = test_statistic(grouped_df)
p_value = (np.sum(np.array(bootstrap_stats) >= observed_stat) + np.sum(np.array(bootstrap_stats) <= -observed_stat)) / n_bootstraps

# Print the results
print("Bootstrap test results:")
print("observed difference in mean distance:", observed_stat)
print("p-value:", p_value)
