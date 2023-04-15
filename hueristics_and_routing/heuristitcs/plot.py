import matplotlib.pyplot as plt
import pandas as pd

# read the spreadsheet data into a pandas DataFrame
data = pd.read_excel('result.xlsx', sheet_name='Sheet1')

# separate the data for each algorithm
alg1_data = data[data['alg_name'] == 'new_heuristic']
alg2_data = data[data['alg_name'] == 'greedy']

# create a figure and axis object
fig, ax = plt.subplots()

# plot the data for algorithm1 as a scatter plot
ax.scatter(alg1_data['time'], alg1_data['distance'], label='Oltea',linestyle="-",marker='o',color='red')

# plot the data for algorithm2 as a scatter plot
ax.scatter(alg2_data['time'], alg2_data['distance'], label='Greedy',linestyle="-",marker='o',color='blue')

ax.plot(alg1_data['time'], alg1_data['distance'], label='Oltea',linestyle="-",marker='o',color='red')

# plot the data for algorithm2 as a scatter plot
ax.plot(alg2_data['time'], alg2_data['distance'], label='Greedy',linestyle="-",marker='o',color='blue')

# set the labels and title for the plot
ax.set_xlabel('Time')
ax.set_ylabel('Distance')
ax.set_title('Comparison of Algorithms 1 and 2')

# show the legend for the plot
ax.legend()

# display the plot
plt.show()