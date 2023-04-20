import pandas as pd
from scipy.stats import ttest_ind

# Load data from Excel sheet
df = pd.read_excel('result.xlsx')
df['alg_name'] = df['alg_name'].astype(str)

# Group the data by number of buses and number of passengers
grouped = df.groupby(['buses', 'passengers'])

for group, data in grouped:
    buses, passengers = group
    # Filter rows for the current group
    data_filtered = data.loc[(data['buses'] == buses) & (data['passengers'] == passengers)]
    
    if 'greedy' in data_filtered['alg_name'].values:
        mean1 = data_filtered.loc[data_filtered['alg_name'] == 'greedy', 'time'].mean()
        std1 = data_filtered.loc[data_filtered['alg_name'] == 'greedy', 'time'].std()
    else:
        mean1, std1 = float('nan'), float('nan')

    if 'new_heuristic' in data_filtered['alg_name'].values:
        mean2 = data_filtered.loc[data_filtered['alg_name'] == 'new_heuristic', 'time'].mean()
        std2 = data_filtered.loc[data_filtered['alg_name'] == 'new_heuristic', 'time'].std()
    else:
        mean2, std2 = float('nan'), float('nan')
    
    # Perform two-sample t-test for time column
    t_stat, p_val = ttest_ind(data_filtered.loc[data_filtered['alg_name'] == 'greedy', 'time'], data_filtered.loc[data_filtered['alg_name'] == 'new_heuristic', 'time'], equal_var=True)
    
    # Check if p-value is less than significance level (e.g., 0.05)
    if p_val < 0.05:
        print(f"For group {group}: New heuristic is better in terms of time.")
    else:
        print(f"For group {group}: No significant difference in time between the two algorithms.")
    
    print(p_val)
    
    # Repeat for distance column
    try:
        mean1 = data_filtered.loc[data_filtered['alg_name'] == 'greedy', 'distance'].mean()
        std1 = data_filtered.loc[data_filtered['alg_name'] == 'greedy', 'distance'].std()
        mean2 = data_filtered.loc[data_filtered['alg_name'] == 'new_heuristic', 'distance'].mean()
        std2 = data_filtered.loc[data_filtered['alg_name'] == 'new_heuristic', 'distance'].std()
    except KeyError:
        mean1, std1, mean2, std2 = float('nan'), float('nan'), float('nan'), float('nan')
    
    t_stat, p_val = ttest_ind(data_filtered.loc[data_filtered['alg_name'] == 'greedy', 'distance'], data_filtered.loc[data_filtered['alg_name'] == 'new_heuristic', 'distance'], equal_var=True)
    
    if p_val < 0.05:
        print(f"For group {group}: New heuristic is better in terms of distance.")
    else:
        print(f"For group {group}: No significant difference in distance between the two algorithms.")
