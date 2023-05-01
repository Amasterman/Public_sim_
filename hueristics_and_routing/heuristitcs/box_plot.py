import pandas as pd
import matplotlib.pyplot as plt

# Load the data into a pandas DataFrame
df = pd.read_excel("result.xlsx")

# Subset the data to include only rows with the same number of buses and passengers
grouped_df = df.groupby(['buses', 'passengers']).filter(lambda x: len(x) == 2)
grouped_df = grouped_df.sort_values(['buses', 'passengers'])

# Calculate the mean time and distance for each algorithm
mean_data = grouped_df.groupby(['alg_name']).mean()

# Create a bar plot to compare the mean time and distance for each algorithm
fig, ax = plt.subplots()
mean_data.plot(kind='bar', ax=ax)
ax.set_ylabel('Time (seconds) / Distance (meters)')
ax.set_title('Comparison of New Heuristic and Greedy Algorithms')
plt.show()