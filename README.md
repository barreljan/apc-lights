# Lights automation
## for use with an SNMP enabled device

This is a simple automated tool, combining 2 scripts for
the simple use of switch on or off 1 or more snmp enabled 
devices.

In this case, a metered and switched APC rack PDU is used
to switch 2 lights on and off. To help this, a job is 
inserted in the crontab of an Linux device (eg. OrangePI).
The job is inserted once manually and after that it resets
itself to the correct time (...twilight_end).

So, a sort of home automation but different.

## Requirements
- Linux environment
- Python 3.x (compatible with 2.7)
- modules: json, requests, python-crontab
- snmp tools (like snmputils for snmpget and snmpset)
- SNMP enabled switch device

### Installing
1) Clone the 2 files, make them executable.
   - Set the email function to your wishes in api_sunset.py
   - Set the correct latitude and longtitude of the param
     'link' in api_sunset.py
   - Set the job user to the correct one
   - Set the job.new accordingly to your installation dir
   - Set the snmp IP's and communities in lights.sh
2) Edit your crontab (crontab -e) and add these lines:
```
0 6 * * * <youruser> /your/dir/api_sunset.py
1 1 * * * <youruser> /your/dir/lights.sh on >/dev/null 2>&1
0 23 * * * <youruser> /your/dir/lights.sh off >/dev/null 2>&1
```
   Set your 'off' time accordingly. The 'on' time is just some
random. It will reset itself eventually.

4) Execute the API call by running "./api_sunset.py"
5) Check the new cron job with "crontab -l"

### Different time schemes
The API gives multiple times in a JSON format. You can choose
your own time for switching on your lights(or device)

```
{
"results":
    {
        "sunrise":"2018-10-08T06:34:22+00:00",
        "sunset":"2018-10-08T17:40:13+00:00",
        "solar_noon":"2018-10-08T12:07:17+00:00",
        "day_length":39951,
        "civil_twilight_begin":"2018-10-08T06:00:05+00:00",
        "civil_twilight_end":"2018-10-08T18:14:30+00:00",
        "nautical_twilight_begin":"2018-10-08T05:20:18+00:00",
        "nautical_twilight_end":"2018-10-08T18:54:17+00:00",
        "astronomical_twilight_begin":"2018-10-08T04:39:57+00:00",
        "astronomical_twilight_end":"2018-10-08T19:34:38+00:00"
    },
"status":"OK"
}
```

For now, it uses the 'nautical_twilight_end' time. Set it
to your prefered time in api_sunset.py

Disclamer:

Yes, the lights.sh could be done in a different manner.
Yes, you can use z-wave/hue/insert-vendor, but if you
already have such APC rack pdu behind your furniture...
