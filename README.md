# RSF Crowd Meter Analysis Tool
![Last Commit](https://img.shields.io/github/last-commit/AidanPraytor/rsf-crowd-analysis)
![Commit Activity](https://img.shields.io/github/commit-activity/w/AidanPraytor/rsf-crowd-analysis)
[Public GitHub repository][git]

Are you tired of thinking you'll beat the crowd to the RSF, just to shuffle around the overflowing gym with nothing but the weight of your disappointment to bench press? I know I am!

This is a project I thought about last year and have only now gotten around to making. It's still in its very early stages, so don't be surprised by the lack of collected data and rudimentary code. That being said, it's my first step towards a fully-fledged app or website that compiles RSF crowd data in order to predict trends in weightroom crowdedness and provide users with optimal times to workout.

## Description
This program scrapes the [RSF website][rsf] for the "Crowd Meter" data. Accommodating for JS load times, `scraper.py` locates and parses an element on the page that displays what "percent full" the weight room currently is. This data is then stored along with the precise date and time of the scrape in `data/allPulls.csv`, as well as a file just for data pulled from that day which is created automatically. The process is automated by `manager.py`, pulling data from the website at regular intervals during the RSF's open hours of the day. The pull interval can be adjusted in terms of "pulls per hour".

## Future Goals
The project is barebones for now, but it is very much under active development. Here are some of my goals for its future:

**Short-term:**
- Incorporate edge case support for holidays and such days when the RSF has odd hours of operation.
- Add timeout exception handling to not halt data collection when page fails to load.
- Data visualization support, including easy switching between day, week, month, year views.
- Optimize the automation. The current implementation is a quick and dirty solution to a surprisingly annoying problem, but I would like for the automation to be far more exact and far less resource consuming. Hoping for something along the lines of a task scheduler system like in Windows.

**Long-term:**
- App/website interface.
- Long-term data collection on a server instead of my computer.
- Crowd predictions that are more than just, "Hey, it was this busy on average for the past few months around this time, so it'll probably be that busy again". Not sure exactly what this entails yet, but hence "long-term".
- Translating data into more digestible ideas. "78% Full", isn't very easy to visualize, but knowing exactly how many people that is or even seeing a diagram representing it is!

## License

MIT

   [git]: <https://github.com/AidanPraytor/rsf-crowd-analysis.git>
   [rsf]: <https://recsports.berkeley.edu/rsf-weight-room-crowd-meter/>
