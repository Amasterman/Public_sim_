import pandas as pd
from scipy.stats import ranksums, kruskal
import numpy as np
from scipy.stats import ttest_ind

# Load the data into a pandas DataFrame
df = pd.read_excel("result.xlsx")

# Subset the data to include only rows with the same number of buses and passengers
grouped_df = df.groupby(['buses', 'passengers']).filter(lambda x: len(x) == 2)
grouped_df = grouped_df.sort_values(['buses', 'passengers'])

# Perform a two-sided Wilcoxon rank-sum test for distance
new_heuristic_distance_data = grouped_df[grouped_df['alg_name'] == 'transfer']['passenger_time']
greedy_distance_data = grouped_df[grouped_df['alg_name'] == 'greedy']['passenger_time']
distance_test_stat, distance_p_value = ranksums(new_heuristic_distance_data, greedy_distance_data)
print("Wilcoxon rank-sum test results for distance:")
print("test statistic:", distance_test_stat)
print("p-value:", distance_p_value)

if distance_p_value < 0.05:
    if distance_test_stat < 0:
        print("The 'transfer' algorithm has better performance than the 'greedy' algorithm for distance.")
    else:
        print("The 'greedy' algorithm has better performance than the 'transfer' algorithm for distance.")
else:
    print("There is no significant difference between the performance of the 'transfer' and 'greedy' algorithms for distance.")

# Perform a Kruskal-Wallis test for time
new_heuristic_time_data = grouped_df[grouped_df['alg_name'] == 'transfer']['distance']
greedy_time_data = grouped_df[grouped_df['alg_name'] == 'greedy']['distance']
time_test_stat, time_p_value = kruskal(new_heuristic_time_data, greedy_time_data)
print("Kruskal-Wallis test results for time:")
print("test statistic:", time_test_stat)
print("p-value:", time_p_value)

if time_p_value < 0.05:
    if time_test_stat < 0:
        print("The 'transfer' algorithm has better performance than the 'greedy' algorithm for time.")
    else:
        print("The 'greedy' algorithm has better performance than the 'transfer' algorithm for time.")
else:
    print("There is no significant difference between the performance of the 'transfer' and 'greedy' algorithms for time.")



# Split the data into two groups based on the algorithm used for time
new_heuristic_time_data = grouped_df[grouped_df['alg_name'] == 'transfer']['passenger_wait']
greedy_time_data = grouped_df[grouped_df['alg_name'] == 'greedy']['passenger_wait']

# Perform a two-sided t-test for time
time_t_stat, time_p_value = ttest_ind(new_heuristic_time_data, greedy_time_data, equal_var=False)

# Print the results for time
print("t-test results for time:")
print("test statistic:", time_t_stat)
print("p-value:", time_p_value)

# Compare the mean values for time
new_heuristic_time_mean = np.mean(new_heuristic_time_data)
greedy_time_mean = np.mean(greedy_time_data)

if new_heuristic_time_mean < greedy_time_mean:
    print("The new heuristic algorithm is more time efficient.")
elif new_heuristic_time_mean > greedy_time_mean:
    print("The greedy algorithm is more time efficient.")
else:
    print("There is no significant difference between the algorithms in terms of time efficiency.")