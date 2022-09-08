import csv
import datetime
import scraper
import time

weekdayHours = (7, 23)
saturdayHours = (8, 18)
sundayHours = (8, 23)

pullsPerHour = 6


def pull_and_write(now):
    with open('data/allPulls.csv', mode='a') as data:
        data_writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow([now.strftime("%Y"), now.strftime("%d"),
                              now.strftime("%a"), now.strftime("%H:%M"), scraper.retrieve()])


def check(cdt):
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
        minutesUntilNextPull = (60 // pullsPerHour)
        print("Data pulled. I'll sleep for " + str(minutesUntilNextPull) + " minute(s), and then pull again!")
        time.sleep(minutesUntilNextPull * 60)
    check(datetime.datetime.now())


check(datetime.datetime.now())