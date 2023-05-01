import pandas as pd
import numpy as np
from scipy.stats import shapiro, mannwhitneyu, ttest_ind

# Read the Excel file into a pandas DataFrame
data = pd.read_excel('result.xlsx')

# Separate the data for each algorithm
alg1_data = data[data['alg_name'] == 'transfer']
alg2_data = data[data['alg_name'] == 'greedy']

# Select only the rows where both the number of buses and passengers are equal for both algorithms
equal_data = alg1_data.merge(alg2_data, on=['buses', 'passengers'])

# Extract the time and distance data for each algorithm
alg1_time = equal_data['passenger_time_x'].values
alg2_time = equal_data['passenger_time_y'].values
alg1_distance = equal_data['distance_x'].values
alg2_distance = equal_data['distance_y'].values

# Shapiro-Wilk test for normality
stat, p = shapiro(alg1_time)
print(f'Algorithm 1 time data normality test result: statistic={stat:.3f}, p-value={p:.5f}')
stat, p = shapiro(alg2_time)
print(f'Algorithm 2 time data normality test result: statistic={stat:.3f}, p-value={p:.5f}')

# Mann-Whitney U test for nonparametric data
stat, p = mannwhitneyu(alg1_time, alg2_time)
print(f'Mann-Whitney U test for time result: statistic={stat:.3f}, p-value={p:.5f}')

# Calculate mean time and distance for each algorithm
alg1_mean_time = np.mean(alg1_time)
alg2_mean_time = np.mean(alg2_time)
alg1_mean_distance = np.mean(alg1_distance)
alg2_mean_distance = np.mean(alg2_distance)

# Print results
print(f"Mean time for Algorithm 1: {alg1_mean_time:.3f}")
print(f"Mean time for Algorithm 2: {alg2_mean_time:.3f}")
print(f"Mean distance for Algorithm 1: {alg1_mean_distance:.3f}")
print(f"Mean distance for Algorithm 2: {alg2_mean_distance:.3f}")

# Determine which algorithm has shorter time and distance
if alg1_mean_time < alg2_mean_time:
    print("Algorithm 1 has shorter time.")
else:
    print("Algorithm 2 has shorter time.")
    
if alg1_mean_distance < alg2_mean_distance:
    print("Algorithm 1 has shorter distance.")
else:
    print("Algorithm 2 has shorter distance.")