#!/usr/bin/python3.5
#
# @author bartjan@pc-mania.nl
# Oct-6,2018

import requests
import json
import smtplib
import sys
import time
from crontab import CronTab

link = 'https://api.sunrise-sunset.org/json?lat=52.840449&lng=-4.972762?&formatted=0'
localtime = time.localtime()

def time_of(input):
    # Get the JSON output from the API
    try:
        data = requests.get(link).text
    except Exception:
        sendmail("Failed to connect to API")
        sys.exit()
    data = json.loads(data)

    # Fetch the wanted time
    try:
        time = str(data['results'][input]).split('T')[1].split('+')[0]
    except Exception:
        sendmail("No usable data is returned, keeping old time")
        sys.exit()

    return time

def reset_crontab(minute,hour):
    cron = CronTab(user='root')

    # Check and remove the old job
    try:
        for job in cron.find_command('lights.sh on'):
            job.delete()
    except Exception:
        sendmail("Old cron job not found, stopping update")
        sys.exit()

    # Set the new job at the given time
    job = cron.new(command='/bin/bash /root/scripts/apc-lights/lights.sh on >/dev/null 2>&1')
    job.minute.on(minute)
    job.hour.on(hour)

    # Save job
    try:
        cron.write()
    except Exception:
        sendmail("Writing new cron failed")
        sys.exit()

def sendmail(msg):
    msg = "Subject: sunset tool warning" + "\n\n" + msg
    server = smtplib.SMTP('smtp.pc-mania.nl',25)
    server.sendmail('opi@pbs.hb.local','bartjan@h-p-c.nl',msg)

###

# Get new time and split in hour/minute
time = time_of('nautical_twilight_end')
hour = int(time.split(':')[0])
if not localtime.tm_isdst:
    # Correct daylight savings
    hour = hour - 1
minute = int(time.split(':')[1])

# Update (so reset) the cronjob
reset_crontab(minute,hour)
