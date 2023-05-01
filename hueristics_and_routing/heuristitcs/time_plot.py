import pandas as pd
import matplotlib.pyplot as plt

# Load the data into a pandas DataFrame
df = pd.read_excel("result.xlsx")

# Subset the data to include only rows with the same number of buses and passengers
grouped_df = df.groupby(['buses', 'passengers']).filter(lambda x: len(x) == 2)
grouped_df = grouped_df.sort_values(['buses', 'passengers'])

# Split the data into two groups based on the algorithm used
new_heuristic_data = grouped_df[grouped_df['alg_name'] == 'transfer']['time']
greedy_data = grouped_df[grouped_df['alg_name'] == 'greedy']['time']

# Generate a box plot to compare the distribution of times for the two algorithms
fig, ax = plt.subplots()
ax.boxplot([new_heuristic_data, greedy_data], labels=['Transfer', 'Greedy'])
ax.set_title('Comparison of Algorithm Times')
ax.set_ylabel('Time (seconds)')
plt.show()