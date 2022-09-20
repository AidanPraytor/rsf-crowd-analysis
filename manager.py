#!/usr/bin/env python3
"""Control portion of project. Handles the automated calling of scraper.py and the writing of
data to data/allPulls.csv.
"""

import csv
import datetime
import os

import scraper
import visualizer
import time
from os import path

weekdayHours = (7, 23)
saturdayHours = (8, 18)
sundayHours = (8, 23)

pullsPerHour = 12

crowdMeter = 'https://safe.density.io/#/displays/dsp_956223069054042646?token' \
             '=shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e '


def pull_and_write(now):
    """Call scraper.retrieve(), write returned data to .csv

    :param now: datetime object containing current year, month, day, hour, minute, second
    """
    year, month, dayOfMonth = now.strftime("%Y"), now.strftime("%m"), now.strftime("%d")
    dayOfWeek, hourMinute = now.strftime("%a"), now.strftime("%H:%M")

    todayFileName = 'data/' + month + dayOfMonth + year + '.csv'
    writeTo = ['data/allPulls.csv', todayFileName]

    pulledData = scraper.retrieve()

    if not path.isfile(todayFileName):
        print("File for today's data not found. Creating one now!")
        with open(todayFileName, mode='w') as data:
            data_writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_writer.writerow(['Date and Time', '% Full'])
    else:
        print("File for today's data found. Writing to " + str(len(writeTo)) + " file(s) now")

    for f in writeTo:
        with open(f, mode='a') as data:
            data_writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_writer.writerow([year + '-' + month + '-' + dayOfMonth + ' ' + hourMinute, pulledData])

    scraper.driver.quit()


def check(cdt, PPH):
    """Controls automated scraping and logging of data.

    Given datetime object, cdt, determines current day-of-week and consequently the RSF hours of
    operation. Determines if the current time is before, after, or during RSF hours. If before,
    determines time until RSF opens, sleeps until then. If after, determines time until next day,
    sleeps until then. If during, calls pull_and_write with current datetime object, then sleeps
    for regular interval determined by PPH (pulls per hour). Function recursively calls itself
    again every time sleep command expires.

    :param PPH: Number of times the program should gather and log data per hour, given that
    it is started on the hour.
    :param cdt: datetime object containing current year, month, day, hour, minute, second
    """
    currentHour = int(cdt.strftime("%H"))
    currentMinute = int(cdt.strftime("%M"))
    currentTime = currentHour + (currentMinute / 60)
    if cdt.strftime("%A") == "Saturday":
        opensAt, closesAt = saturdayHours[0], saturdayHours[1]
    elif cdt.strftime("%A") == "Sunday":
        opensAt, closesAt = sundayHours[0], sundayHours[1]
    else:
        opensAt, closesAt = weekdayHours[0], weekdayHours[1]

    if currentTime < opensAt:
        timeUntilOpen = (opensAt - currentTime) * 3600
        print("The RSF isn't open yet. I'll sleep for " + str(timeUntilOpen) + " seconds until it is!")
        time.sleep(timeUntilOpen)
    elif currentTime > closesAt:
        timeUntilNextDay = ((24 - currentTime) * 3600) + 60  # just for good measure
        print("The RSF has already closed. I'll sleep for " + str(timeUntilNextDay)
              + " seconds until tomorrow and check again!")
        time.sleep(timeUntilNextDay)
    else:
        pull_and_write(cdt)
        minutesUntilNextPull = (60 // PPH)
        print("Data pulled. I'll sleep for " + str(minutesUntilNextPull) + " minute(s), and then pull again!")
        time.sleep(minutesUntilNextPull * 60)
    check(datetime.datetime.now(), PPH)


def interact():
    print("Welcome. Use '0' to go back in any of the following prompts.")
    record_data = input("Record data? [y/n]: ")
    if record_data == 'y':
        check(datetime.datetime.now(), pullsPerHour)
    elif record_data == 'n':
        control_visualizer()
    elif record_data == '0':
        print("Goodbye.")
    else:
        print("Unknown entry. Please try again.")
        interact()


def control_visualizer():
    print("[1] To visualize all available data.\n[2] To visualize a specific day.")
    q1 = input("Enter an option from above:")
    if q1 == '1':
        visualizer.visualize_with_pd('data/allPulls.csv')
    elif q1 == '2':
        days = os.listdir('data')
        numeratedDays = ["[" + str(i + 1) + "] " + days[i] for i in range(len(days))]
        for day in numeratedDays:
            print(day)
        chosenDay = input("Select desired day with associated number: ")
        if input == '0':
            control_visualizer()
        try:
            chosenDayFile = days[int(chosenDay) - 1]
            visualizer.visualize_with_pd('data/' + chosenDayFile)
        except IndexError:
            print("Input invalid. Please try again.")
            control_visualizer()

    elif q1 == '0':
        interact()
    else:
        print("Unknown entry. Please try again.")
        control_visualizer()


interact()
