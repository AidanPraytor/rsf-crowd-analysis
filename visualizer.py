import matplotlib.pyplot as plt
import csv
import pandas as pd


def visualize_day(file):
    x = []
    y = []

    with open(file, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        next(plots)

        for row in plots:
            x.append(row[4])
            y.append(row[5])

    plt.bar(x, y)
    plt.xlabel('Time')
    plt.ylabel('% Full')
    plt.title('Day Visualizer')
    plt.legend()
    plt.show()


def visualize_with_pd(file):
    data = pd.read_csv(file)
    data['Date and Time'] = pd.to_datetime(data['Date and Time'])
    data.sort_values('Date and Time', inplace=True)

    date = data['Date and Time']
    percent = data['% Full']

    plt.plot_date(date, percent, linestyle='solid')

    plt.gcf().autofmt_xdate()

    plt.xlabel('Date and Time')
    plt.ylabel('% Full')

    plt.show()


#visualize_with_pd('data/09112022.csv')


