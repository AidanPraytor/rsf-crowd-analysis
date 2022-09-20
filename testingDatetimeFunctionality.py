import csv
import datetime
import pandas as pd
import matplotlib.pyplot as plt


def read_with_csv():
    now = datetime.datetime.now()

    year, month, dayOfMonth = now.strftime("%Y"), now.strftime("%m"), now.strftime("%d")
    dayOfWeek, hourMinute = now.strftime("%a"), now.strftime("%H:%M")

    with open('new-format-data/newAllPulls.csv', mode='a') as data:
        data_writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow([year + '-' + month + '-' + dayOfMonth, hourMinute, "98"])

'''
data = pd.read_csv('new-format-data/newAllPulls.csv')
data['Date and Time'] = pd.to_datetime(data['Date and Time'])
data.sort_values('Date and Time', inplace=True)

date = data['Date and Time']
percent = data['% Full']

plt.plot_date(date, percent, linestyle='solid')

plt.gcf().autofmt_xdate()

plt.xlabel('Date and Time')
plt.ylabel('% Full')

plt.show()
'''