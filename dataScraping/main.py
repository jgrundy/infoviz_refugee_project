#!/usr/bin/env python
from getcountry import GetCountry as gc
from processtweets import getdata
import csv
import os
import re
import sys
# from string import punctuation


def main():
    try:
        os.remove("../input/{0}.csv".format(sys.argv[1]))
    except:
        pass
    tweet_count = 0
    try:
        with open("../input/{0}.txt".format(sys.argv[1]), 'r') as inputfile:
            for tweet in inputfile:
                if len(tweet) > 1:
                    message, location, country, time_zone = getdata(tweet)
                    location = location.replace(" ", "-")
                    if country == " ":
                        try:
                            gapi_country = gc.getcountry(location)
                        except:
                            print("Using time zone to get country")
                            gapi_country = time_zone.split(" ")[-1]
                            gapi_country = (re.findall(
                                r"[A-Za-z]", gapi_country))
                            gapi_country = "".join(gapi_country)
                            print(gapi_country)
                        if gapi_country:
                            country = gapi_country
                            print(country)
                        else:
                            country = "N/A"
                    csvfile = open("../input/{0}.csv".format(sys.argv[1]), "a")
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([message, country])
                    csvfile.close()
                    tweet_count += 1
                    print("tweets processed:", tweet_count)
    except IndexError:
        print 'format: python main.py textFileName'
if __name__ == '__main__':
    main()
