IR Transmitter web controlled, code really needs to be cleaned up and needs better documentation, but it's working at the moment.

The web interface has the following end points:
```
   /list        - Show List of Supported Keys
   /key/KEYID   - Transmit KEYID
   /channel/### - Transmit Digits Followed by KEYOK
   /reboot      - Reboot IR Controller
```
To change the channel to 123 I use curl from the server to http://192.168.1.129/channel/123 and the ESP sends EXIT, EXIT, 1, 2, 3, ENTER

I reboot the device remotely using http://192.168.1.129/reboot every night at 3:12 AM

And I have a cron job that runs 4 times an hour (8, 23, 38, 53) that checks to see if MythTV is recording, and if so sends the /key/D as I've found that during normal watching, the key D does nothing, but does keep the box alive so I don't get an 'Are you still watching' message in my recordings.