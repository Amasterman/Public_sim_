import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import linregress


# KEEEP THIS
# Read the Excel file into a pandas DataFrame
data = pd.read_excel('result.xlsx')
alg1_data = data[data['alg_name'] == 'new_heuristic']
alg2_data = data[data['alg_name'] == 'greedy']
# Select only the rows where both the number of buses and passengers are equal for both algorithms
equal_data = alg1_data.merge(alg2_data, on=['buses', 'passengers'])

# Create a scatter plot of distance vs time, color-coded by algorithm
plt.scatter(equal_data['distance_x'], equal_data['time_x'], c='blue', label='Transfer')
plt.scatter(equal_data['distance_y'], equal_data['time_y'], c='red', label='Greedy')

# Calculate and plot the regression lines for each algorithm
x = equal_data['distance_x']
y = equal_data['time_x']
slope, intercept, r_value, p_value, std_err = linregress(x, y)
plt.plot(x, slope*x + intercept, color='blue')

x = equal_data['distance_y']
y = equal_data['time_y']
slope, intercept, r_value, p_value, std_err = linregress(x, y)
plt.plot(x, slope*x + intercept, color='red')

plt.xlabel('Distance')
plt.ylabel('Time')
plt.title('Performance of Algorithms with Equal Bus and Passenger Counts')
plt.legend()
plt.show()







# tacked bar chart
# plt.bar(alg1_data['passengers'], alg1_data['time'], color='blue')
# plt.bar(alg1_data['passengers'], alg1_data['distance'], color='lightblue', bottom=alg1_data['time'])
# plt.bar(alg2_data['passengers'], alg2_data['time'], color='red')
# plt.bar(alg2_data['passengers'], alg2_data['distance'], color='pink', bottom=alg2_data['time'])
# plt.xlabel('Buses')
# plt.ylabel('Time/Distance')
# plt.title('Comparison of Algorithms')
# plt.legend(['Algorithm 1 (Time)', 'Algorithm 1 (Distance)', 'Algorithm 2 (Time)', 'Algorithm 2 (Distance)'])
# plt.show()














# # read the spreadsheet data into a pandas DataFrame
# data = pd.read_excel('result.xlsx', sheet_name='Sheet1')

# data = data.sort_values(by=['time'])

# # separate the data for each algorithm
# alg1_data = data[data['alg_name'] == 'new_heuristic']
# alg2_data = data[data['alg_name'] == 'greedy']

# # create a figure and axis object
# fig, ax = plt.subplots()

# # plot the data for algorithm1 as a scatter plot
# ax.scatter(alg1_data['time'], alg1_data['distance'], label='Oltea',linestyle="-",marker='o',color='red')

# # plot the data for algorithm2 as a scatter plot
# ax.scatter(alg2_data['time'], alg2_data['distance'], label='Greedy',linestyle="-",marker='o',color='blue')

# ax.plot(alg1_data['time'], alg1_data['distance'], label='Oltea',linestyle="-",marker='o',color='red')

# # plot the data for algorithm2 as a scatter plot
# ax.plot(alg2_data['time'], alg2_data['distance'], label='Greedy',linestyle="-",marker='o',color='blue')

# # set the labels and title for the plot
# ax.set_xlabel('Time')
# ax.set_ylabel('Distance')
# ax.set_title('Comparison of Algorithms 1 and 2')

# # show the legend for the plot
# ax.legend()

# # display the plot
# plt.show()