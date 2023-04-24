import pandas as pd
from scipy.stats import mannwhitneyu

# Load the dataset into a pandas DataFrame
df = pd.read_excel("result.xlsx")

# Loop through each combination of buses and passengers
for buses in df['buses'].unique():
    for passengers in df['passengers'].unique():
        # Subset the data where the number of buses and passengers are the same for both algorithms
        new_heuristic_data = df[(df['alg_name'] == 'new_heuristic') & (df['buses'] == buses) & (df['passengers'] == passengers)]
        greedy_data = df[(df['alg_name'] == 'greedy') & (df['buses'] == buses) & (df['passengers'] == passengers)]
        
        # Perform the Mann-Whitney U test on the time data
        time_stat, time_p_value = mannwhitneyu(new_heuristic_data['time'], greedy_data['time'])
        if time_p_value < 0.05:
            print(f'Buses: {buses}, Passengers: {passengers}, Time p-value: {time_p_value}, new_heuristic is better')
        else:
            print(f'Buses: {buses}, Passengers: {passengers}, Time p-value: {time_p_value}, greedy is better')
        
        # Perform the Mann-Whitney U test on the distance data
        dist_stat, dist_p_value = mannwhitneyu(new_heuristic_data['distance'], greedy_data['distance'])
        if dist_p_value < 0.05:
            print(f'Buses: {buses}, Passengers: {passengers}, Distance p-value: {dist_p_value}, new_heuristic is better')
        else:
            print(f'Buses: {buses}, Passengers: {passengers}, Distance p-value: {dist_p_value}, greedy is better')