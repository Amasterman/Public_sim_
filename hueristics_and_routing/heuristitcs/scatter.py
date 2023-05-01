import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_excel("result.xlsx")

# Function to create scatter plots
def create_scatter_plot(x, y, data, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x=x, y=y, hue="alg_name", style="alg_name", alpha=0.8)
    sns.lineplot(data=data, x=x, y=y, hue="alg_name", alpha=0.5, legend=False)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(title="Algorithm")
    plt.show()

# 1. Passenger Time vs. Distance
create_scatter_plot("distance", "passenger_time", data,
                    "Passenger Time vs. Distance",
                    "Distance", "Passenger Time")

# 2. Transfers vs. Dissatisfied Passengers----------------------------------------------------- good
create_scatter_plot("dissatisfied", "passengers", data,
                    "Passengers vs. Dissatisfied Passengers",
                    "Dissatisfied Passengers", "Passengers")

# 3. Bus Wait vs. Passenger Wait
create_scatter_plot("passenger_wait", "bus_wait", data,
                    "Bus Wait vs. Passenger Wait",
                    "Passenger Wait", "Bus Wait")

# 4. Passenger Time vs. Number of Passengers ----------------------------------------------------- good
create_scatter_plot("passengers", "passenger_time", data,
                    "Passenger Time vs. Number of Passengers",
                    "Number of Passengers", "Passenger Time")

# 5. Distance vs. Number of Buses
create_scatter_plot("buses", "distance", data,
                    "Distance vs. Number of Buses",
                    "Number of Buses", "Distance")