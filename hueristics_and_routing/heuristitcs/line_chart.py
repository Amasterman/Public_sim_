import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_excel("result.xlsx")

# Function to create line charts
def create_line_chart(x, y, data, title, xlabel, ylabel, hue=None):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=data, x=x, y=y, hue=hue, ci=None)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(title="Algorithm")
    plt.show()

# Group data by algorithm, number of buses, and number of passengers, then calculate the mean
grouped_data = data.groupby(["alg_name", "buses", "passengers"]).mean().reset_index()

# Example line charts
# 1. Average Distance by Number of Buses
create_line_chart("buses", "distance", grouped_data,
                  "Average Distance by Number of Buses",
                  "Number of Buses", "Average Distance", hue="alg_name")

# 2. Average Passenger Time by Number of Passengers
create_line_chart("passengers", "passenger_time", grouped_data,
                  "Average Passenger Time by Number of Passengers",
                  "Number of Passengers", "Average Passenger Time", hue="alg_name")

# 3. Average Passenger Wait Time by Number of Buses
create_line_chart("buses", "passenger_wait", grouped_data,
                  "Average Passenger Wait Time by Number of Buses",
                  "Number of Buses", "Average Passenger Wait Time", hue="alg_name")

# 4. Average Dissatisfied Passengers by Number of Passengers
create_line_chart("passengers", "dissatisfied", grouped_data,
                  "Average Dissatisfied Passengers by Number of Passengers",
                  "Number of Passengers", "Average Dissatisfied Passengers", hue="alg_name")

# 5. Average Transfers by Number of Buses
create_line_chart("buses", "transfers", grouped_data,
                  "Average Transfers by Number of Buses",
                  "Number of Buses", "Average Transfers", hue="alg_name")
