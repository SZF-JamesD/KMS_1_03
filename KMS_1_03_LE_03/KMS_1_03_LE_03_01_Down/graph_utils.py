import matplotlib.pyplot as plt
import numpy as np
from file_utils import read_csv_data

def show_graph():

    months, gasoline, diesel = read_csv_data("monthly_fuel_consumption.csv")

    barWidth = 0.25
    fig = plt.figure(figsize = (12, 8))


    br1 = np.arange(len(gasoline))
    br2 = [x + barWidth for x in br1]

    plt.bar(br1, gasoline, color ='r', width= barWidth, edgecolor = 'gray', label = "Gasoline")
    plt.bar(br2, diesel, color = 'black', width= barWidth, edgecolor = 'gray', label = "Diesel")


    plt.xlabel("Months", fontweight = 'bold', fontsize = 12)
    plt.ylabel("Liters Used", fontweight = 'bold', fontsize = 12)
    plt.xticks([r + barWidth for r in range(len(gasoline))], list(months))

    plt.legend()
    return fig

if __name__ == "__main__":
    show_graph()