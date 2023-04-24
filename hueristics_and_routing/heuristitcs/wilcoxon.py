import pandas as pd
import numpy as np
from scipy.stats import ranksums

# Load the data into a pandas DataFrame
df = pd.read_excel("result.xlsx")

# Subset the data to include only rows with the same number of buses and passengers
grouped_df = df.groupby(['buses', 'passengers']).filter(lambda x: len(x) == 2)
grouped_df = grouped_df.sort_values(['buses', 'passengers'])

# Define a function to calculate the test statistic for distance
def distance_test_statistic(data):
    new_heuristic_data = data[data['alg_name'] == 'new_heuristic']['distance']
    greedy_data = data[data['alg_name'] == 'greedy']['distance']
    return np.mean(new_heuristic_data) - np.mean(greedy_data)

# Split the data into two groups based on the algorithm used for distance
new_heuristic_distance_data = grouped_df[grouped_df['alg_name'] == 'new_heuristic']['distance']
greedy_distance_data = grouped_df[grouped_df['alg_name'] == 'greedy']['distance']

# Perform a two-sided Wilcoxon rank-sum test for distance
distance_test_stat, distance_p_value = ranksums(new_heuristic_distance_data, greedy_distance_data)

# Print the results for distance
print("Wilcoxon rank-sum test results for distance:")
print("test statistic:", distance_test_stat)
print("p-value:", distance_p_value)

# Define a function to calculate the test statistic for time
def time_test_statistic(data):
    new_heuristic_data = data[data['alg_name'] == 'new_heuristic']['time']
    greedy_data = data[data['alg_name'] == 'greedy']['time']
    return np.mean(new_heuristic_data) - np.mean(greedy_data)

# Split the data into two groups based on the algorithm used for time
new_heuristic_time_data = grouped_df[grouped_df['alg_name'] == 'new_heuristic']['time']
greedy_time_data = grouped_df[grouped_df['alg_name'] == 'greedy']['time']

# Perform a two-sided Wilcoxon rank-sum test for time
time_test_stat, time_p_value = ranksums(new_heuristic_time_data, greedy_time_data)

# Print the results for time
print("Wilcoxon rank-sum test results for time:")
print("test statistic:", time_test_stat)
print("p-value:", time_p_value)

# Determine which algorithm is better based on the p-values for distance and time
if distance_p_value < 0.05:
    if distance_test_stat < 0:
        print("The new heuristic algorithm performs better than the greedy algorithm in terms of distance.")
    else:
        print("The greedy algorithm performs better than the new heuristic algorithm in terms of distance.")
else:
    print("There is not enough evidence to conclude that one algorithm performs better than the other in terms of distance.")

if time_p_value < 0.05:
    if time_test_stat > 0:
        print("The new heuristic algorithm performs better than the greedy algorithm in terms of time.")
    else:
        print("The greedy algorithm performs better than the new heuristic algorithm in terms of time.")
else:
    print("There is not enough evidence to conclude that one algorithm performs better than the other in terms of time.")