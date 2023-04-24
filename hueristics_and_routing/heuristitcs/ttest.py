
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Load the data into a pandas DataFrame
df = pd.read_excel("result.xlsx")

# Subset the data to include only rows with the same number of buses and passengers
grouped_df = df.groupby(['buses', 'passengers']).filter(lambda x: len(x) == 2)
grouped_df = grouped_df.sort_values(['buses', 'passengers'])

# Define a function to calculate the test statistic
def test_statistic(data):
    new_heuristic_data = data[data['alg_name'] == 'new_heuristic']['time']
    greedy_data = data[data['alg_name'] == 'greedy']['time']
    return np.mean(new_heuristic_data) - np.mean(greedy_data)

# Split the data into two groups based on the algorithm used
new_heuristic_data = grouped_df[grouped_df['alg_name'] == 'new_heuristic']['time']
greedy_data = grouped_df[grouped_df['alg_name'] == 'greedy']['time']

# Perform a two-sided t-test
t_stat, p_value = ttest_ind(new_heuristic_data, greedy_data, equal_var=False)

# Print the results
print("Two-sample t-test results:")
print("test statistic:", t_stat)
print("p-value:", p_value)