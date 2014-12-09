#!/usr/bin/env python2
"""
A python script to announce events, scheduled in an iCal URL, provided by Remember the Milk.
Author: David Koppel <kuroishi@gmail.com>
"""

import os
import urllib2
import datetime
from icalendar import Calendar, Event

calurl = ""

def fetchcal(url):
    """ Given a url to an ical data source, fetch it and return it as a Calendar object """
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = response.read()
    return Calendar.from_ical(data)

def fetchofflinecal(filename):
    """ Given a relative path to an ical data source, fetch it and return it as a Calendar object """
    directory =  os.getcwd()
    data = open(os.path.join(directory, filename), 'rb').read()
    return Calendar.from_ical(data)

def fetchevents(cal):
    """ Given a Calendar object, return it's Event subcomponent. """
    return cal.walk('VEVENT')

def announce(msg):
    """ Announce an upgrade """
    channel = "\#support"
    command = "/usr/local/bin/rbot-notify" + " -d " + channel + " '" + msg + "'" 
    os.system(command)
    return None

def fiveminutewarning(events):
    """ Warn when an upgrade is approaching in the next 5 minutes """
    for x in events:
        etime = x.decoded('dtstart')
        if type(etime) == datetime.datetime:
            td = etime - datetime.datetime.now() # time delta for event dtstart minus now
        # this really makes no sense, but I haven't figured out how we want to handle scheduled events with date but no time.
        elif type(etime) == datetime.date:
            td = etime - datetime.datetime.now().date()
        else:
            #raise Exception('invalid date types.')
	    pass
        if td <= datetime.timedelta(minutes=5) and td > datetime.timedelta(minutes=0):
            msg = "\0034Scheduled Event Imminent: \00316" + str(x.decoded('summary')) + " @ \00303" + str(etime) 
            announce(msg)
    return None

def main():
    #cal = fetchofflinecal('test.ics')
    cal = fetchcal(calurl)
    events = fetchevents(cal)
    fiveminutewarning(events)

if __name__ == '__main__':
    main()
