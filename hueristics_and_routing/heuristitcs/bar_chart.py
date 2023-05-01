import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_excel("result.xlsx")

# Function to create bar charts
def create_bar_chart(x, y, data, title, xlabel, ylabel, hue=None):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=data, x=x, y=y, hue=hue, ci=None)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(title="Algorithm")
    plt.show()

# Group data by algorithm, number of buses, and number of passengers, then calculate the mean
grouped_data = data.groupby(["alg_name", "buses", "passengers"]).mean().reset_index()

# Example bar charts
# # 1. Average Distance by Algorithm
# create_bar_chart("alg_name", "distance", grouped_data,
#                  "Average Distance by Algorithm",
#                  "Algorithm", "Average Distance")

# # 2. Average Passenger Time by Algorithm and Number of Buses
# create_bar_chart("alg_name", "passenger_time", grouped_data,
#                  "Average Passenger Time by Algorithm and Number of Buses",
#                  "Algorithm", "Average Passenger Time", hue="buses")

# # 3. Average Passenger Wait Time by Algorithm and Number of Passengers
# create_bar_chart("alg_name", "passenger_wait", grouped_data,
#                  "Average Passenger Wait Time by Algorithm and Number of Passengers",
#                  "Algorithm", "Average Passenger Wait Time", hue="passengers")

# # 4. Average Dissatisfied Passengers by Algorithm and Number of Buses
# create_bar_chart("alg_name", "dissatisfied", grouped_data,
#                  "Average Dissatisfied Passengers by Algorithm and Number of Buses",
#                  "Algorithm", "Average Dissatisfied Passengers", hue="buses")

# # 5. Average Transfers by Algorithm and Number of Passengers
# create_bar_chart("alg_name", "transfers", grouped_data,
#                  "Average Transfers by Algorithm and Number of Passengers",
#                  "Algorithm", "Average Transfers", hue="passengers")

# 1. Average Time by Algorithm
create_bar_chart("alg_name", "time", grouped_data,
                 "Average Time by Algorithm",
                 "Algorithm", "Average Time")
