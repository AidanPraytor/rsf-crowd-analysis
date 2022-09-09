#!/usr/bin/env python3
"""Control portion of project. Handles the automated calling of scraper.py and the writing of
data to data/allPulls.csv.
"""

import csv
import datetime
import scraper
import time

weekdayHours = (7, 23)
saturdayHours = (8, 18)
sundayHours = (8, 23)

pullsPerHour = 12


def pull_and_write(now):
    """Call scraper.retrieve(), write returned data to .csv

    :param now: datetime object containing current year, month, day, hour, minute, second
    """
    with open('data/allPulls.csv', mode='a') as data:
        data_writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow([now.strftime("%Y"), now.strftime("%d"),
                              now.strftime("%a"), now.strftime("%H:%M"),
                              scraper.retrieve(url='https://safe.density.io/#/displays/dsp_956223069054042646?token'
                                                   '=shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e')])


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


check(datetime.datetime.now(), pullsPerHour)
