import pandas as pd
import numpy as np
from scipy.stats import ranksums

# Load the data into a pandas DataFrame
df = pd.read_excel("result.xlsx")

# Subset the data to include only rows with the same number of buses and passengers
grouped_df = df.groupby(['buses', 'passengers']).filter(lambda x: len(x) == 2)
grouped_df = grouped_df.sort_values(['buses', 'passengers'])

# Define a function to calculate the test statistic
def test_statistic(data):
    new_heuristic_data = data[data['alg_name'] == 'new_heuristic']['distance']
    greedy_data = data[data['alg_name'] == 'greedy']['distance']
    return np.mean(new_heuristic_data) - np.mean(greedy_data)

# Split the data into two groups based on the algorithm used
new_heuristic_data = grouped_df[grouped_df['alg_name'] == 'new_heuristic']['distance']
greedy_data = grouped_df[grouped_df['alg_name'] == 'greedy']['distance']

# Perform a two-sided Wilcoxon rank-sum test
test_stat, p_value = ranksums(new_heuristic_data, greedy_data)

print("Wilcoxon rank-sum test results:")
print("test statistic:", test_stat)
print("p-value:", p_value)

# Determine which algorithm is better based on the p-value
if p_value < 0.05:
    if test_stat > 0:
        print("The new heuristic algorithm performs better than the greedy algorithm.")
    else:
        print("The greedy algorithm performs better than the new heuristic algorithm.")
else:
    print("There is not enough evidence to conclude that one algorithm performs better than the other.")