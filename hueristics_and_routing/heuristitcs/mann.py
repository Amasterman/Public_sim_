import pandas as pd
import numpy as np
from scipy.stats import shapiro, mannwhitneyu, ttest_ind

# Read the Excel file into a pandas DataFrame
data = pd.read_excel('result.xlsx')

# Separate the data for each algorithm
alg1_data = data[data['alg_name'] == 'new_heuristic']
alg2_data = data[data['alg_name'] == 'greedy']

# Select only the rows where both the number of buses and passengers are equal for both algorithms
equal_data = alg1_data.merge(alg2_data, on=['buses', 'passengers'])

# Extract the time data for each algorithm
alg1_time = equal_data['distance_x'].values
alg2_time = equal_data['distance_y'].values

# Shapiro-Wilk test for normality
stat, p = shapiro(alg1_time)
print(f'Algorithm 1 time data normality test result: statistic={stat:.3f}, p-value={p:.5f}')
stat, p = shapiro(alg2_time)
print(f'Algorithm 2 time data normality test result: statistic={stat:.3f}, p-value={p:.5f}')

# Mann-Whitney U test for nonparametric data
stat, p = mannwhitneyu(alg1_time, alg2_time)
print(f'Mann-Whitney U test result: statistic={stat:.3f}, p-value={p:.5f}')

# Two-sample t-test for parametric data (assuming equal variances)
stat, p = ttest_ind(alg1_time, alg2_time, equal_var=True)
print(f'Two-sample t-test result: statistic={stat:.3f}, p-value={p:.5f}')