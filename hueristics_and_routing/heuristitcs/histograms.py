import pandas as pd
import numpy as np
from scipy.stats import ranksums
from scipy.stats import shapiro
import matplotlib.pyplot as plt

# Load the data into a pandas DataFrame
df = pd.read_excel("result.xlsx")

# Subset the data to include only rows with the same number of buses and passengers
grouped_df = df.groupby(['buses', 'passengers']).filter(lambda x: len(x) == 2)
grouped_df = grouped_df.sort_values(['buses', 'passengers'])

# Define a function to check the normality of the data using the Shapiro-Wilk test
def check_normality(data):
    stat, p = shapiro(data)
    if p > 0.05:
        return "Normally distributed (p-value: {:.4f})".format(p)
    else:
        return "Not normally distributed (p-value: {:.4f})".format(p)

# Split the data into two groups based on the algorithm used for distance
new_heuristic_distance_data = grouped_df[grouped_df['alg_name'] == 'transfer']['distance']
greedy_distance_data = grouped_df[grouped_df['alg_name'] == 'greedy']['distance']
new_heuristic_time_data = grouped_df[grouped_df['alg_name'] == 'transfer']['time']
greedy_time_data = grouped_df[grouped_df['alg_name'] == 'greedy']['time']

# Check the normality of the distance data and plot a histogram
print("Normality test for distance data:")
print("New heuristic:", check_normality(new_heuristic_distance_data))
print("Greedy:", check_normality(greedy_distance_data))
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].hist(new_heuristic_distance_data, bins=20, alpha=0.5, color='red')
axs[0].set_title('New Heuristic')
axs[0].set_xlabel('Distance')
axs[0].set_ylabel('Frequency')
axs[1].hist(greedy_distance_data, bins=20, alpha=0.5, color='blue')
axs[1].set_title('Greedy')
axs[1].set_xlabel('Distance')
axs[1].set_ylabel('Frequency')
plt.suptitle('Histogram of Distance Data')
plt.show()

# Check the normality of the time data and plot a histogram
print("Normality test for time data:")
print("New heuristic:", check_normality(new_heuristic_time_data))
print("Greedy:", check_normality(greedy_time_data))
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].hist(new_heuristic_time_data, bins=20, alpha=0.5, color='red')
axs[0].set_title('New Heuristic')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('Frequency')
axs[1].hist(greedy_time_data, bins=20, alpha=0.5, color='blue')
axs[1].set_title('Greedy')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('Frequency')
plt.suptitle('Histogram of Time Data')
plt.show()
