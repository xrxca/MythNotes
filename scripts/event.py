#!/usr/bin/python3
"""
    Handler for all mythtv events, most are currently ignored in my system
    Yes there are a couple custom libraries missing, I'll update them online soon?
"""
import configparser
import optparse
import os
import requests
import sys
import tempfile
from xrxutils.dotdict import *
from datetime import datetime
from syslog import openlog, syslog
from pprint import pprint

# Should really be stored in the config
iplist = {
    1: '192.168.1.129',
    2: '192.168.1.128'
    }

inifile = '/etc/mythtv/config.ini'
db = None
api_url = 'http://localhost:6744/'
endpoints = {
        'Encoders': {
            'type': 'GET',
            'path': 'Dvr/GetEncoderList'
            }
        }

def main(args=None):
    openlog(ident="MythEvent")
    report = False
    extra = ""
    # logargv()
    (options, args) = _parse_options()

    match options.eventname:
        case "REC_PENDING":
            if options.secs == '120':
                wake_up_box(options, args)
        case "REC_PREFAIL":
            pass
        case "REC_FAILING":
            report = True
            extra = options.cardid
        case "REC_STARTED":
            pass
        case "REC_STARTED_WRITING":
            pass
        case "REC_FINISHED":
            pass
        case "REC_DELETED":
            pass
        case "REC_EXPIRED":
            pass
        case "LIVETV_STARTED":
            pass
        case "LIVETV_ENDED":
            pass
        case "PLAY_STARTED":
            pass
        case "PLAY_STOPPED":
            pass
        case "PLAY_PAUSED":
            pass
        case "PLAY_UNPAUSED":
            pass
        case "PLAY_CHANGED":
            pass
        case "TUNING_SIGNAL_TIMEOUT":
            extra = options.chanid
            report = True
            pass
        case "MASTER_STARTED":
            pass
        case "MASTER_SHUTDOWN":
            pass
        case "CLIENT_CONNECTED":
            pass
        case "CLIENT_DISCONNECTED":
            pass
        case "SLAVE_CONNECTED":
            pass
        case "SLAVE_DISCONNECTED":
            pass
        case "NET_CTRL_CONNECTED":
            pass
        case "NET_CTRL_DISCONNECTED":
            pass
        case "MYTHFILLDATABASE_RAN":
            update_channels()
            pass
        case "SCHEDULER_RAN":
            pass
        case "SETTINGS_CACHE_CLEARED":
            pass
        case "SCREEN_TYPE":
            """ Screen Created or Destroyed """
            pass
        case "THEME_INSTALLED":
            pass
        case "xKEY_01":
            pass
        case "xKEY_02":
            pass
        case "xKEY_03":
            pass
        case "xKEY_04":
            pass
        case "xKEY_05":
            pass
        case "xKEY_06":
            pass
        case "xKEY_07":
            pass
        case "xKEY_08":
            pass
        case "xKEY_09":
            pass
        case "xKEY_10":
            pass
        case "xCEC_COMMAND_RECEIVED":
            pass
        case _:
            report = True
            logoptions(options,args)
    if report:
        syslog(f"Event: {options.eventname} {extra}")
                

def update_channels():
    """
    Call a MySQL fuction that copies a time offset channel that isn't listing in Schedules direct, 
    and add a few extras after each MythFillDatabase update
    """
    opendb()
    cursor = db.cursor()
    result = cursor.execute("CALL local_channel_update();")
    if result == 0:
        syslog(f"Updated Local Channels")
    else:
        syslog(f"Local Channel Update Failed")


def wake_up_box(options, args):
    # Send Key D to box that will record in two minutes to wake it up
    syslog(f"Wake Up: HDPVR{options.cardid}")
    ip = iplist[int(options.cardid)];
    requests.get(f"http://{ip}/key/D")


def opendb():
    global db
    if db: return
    import pymysql
    import xmltodict
    import atexit
    with open(config.CONFIG.xml,"r") as fd:
        configxml = xmltodict.parse(fd.read())
    db = pymysql.connect(
            host=configxml["Configuration"]["Database"]["Host"], 
            user=configxml["Configuration"]["Database"]["UserName"], 
            password=configxml["Configuration"]["Database"]["Password"], 
            db=configxml["Configuration"]["Database"]["DatabaseName"],
            port=int(configxml["Configuration"]["Database"]["Port"])
            )
    atexit.register(closedb)

def closedb():
    db.close();

def loadconfig():
    global configini, config, dbinfo
    configini = configparser.ConfigParser(dict_type=XrXDotDict)
    configini.read(inifile)
    config = configini._sections

def saveconfig():
    with tempfile.NamedTemporaryFile(mode="w",delete=False) as tmp:
        configini.write(tmp)
        os.rename(tmp.name,inifile)

def _parse_options(args=None):
    usage = "usage: %prog [options] arg"
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("--eventname", action="store")
    parser.add_option("--cardid", action="store")
    parser.add_option("--category", action="store")
    parser.add_option("--chanid", action="store")
    parser.add_option("--dir", action="store")
    parser.add_option("--endtime", action="store")
    parser.add_option("--episode", action="store")
    parser.add_option("--file", action="store")
    parser.add_option("--findid", action="store")
    parser.add_option("--hostname", action="store")
    parser.add_option("--jobid", action="store")
    parser.add_option("--originalairdate", action="store")
    parser.add_option("--parentid", action="store")
    parser.add_option("--partnumber", action="store")
    parser.add_option("--parttotal", action="store")
    parser.add_option("--playgroup", action="store")
    parser.add_option("--reactivate", action="store")
    parser.add_option("--recgroup", action="store")
    parser.add_option("--recid", action="store")
    parser.add_option("--recordedid", action="store")
    parser.add_option("--rectype", action="store")
    parser.add_option("--season", action="store")
    parser.add_option("--secs", action="store")
    parser.add_option("--sender", action="store")
    parser.add_option("--starttime", action="store")
    parser.add_option("--subtitle", action="store")
    parser.add_option("--syndicatedepisode", action="store")
    parser.add_option("--title", action="store")
    parser.add_option("--totalepisodes", action="store")
    parser.add_option("--verboselevel", action="store")
    parser.add_option("--videodevice", action="store")
    parser.add_option("--verbose", action="store", default="general")
    parser.add_option("--loglevel", action="store", default="info")
    parser.add_option("--quiet", action="store_true", default=False)
    parser.add_option("--syslog", action="store", default="local7")

    (options, args) = parser.parse_args()

    for opt in options.__dict__:
        if options.__dict__[opt] == f"%{opt.upper()}%":
            options.__dict__[opt] = None
    return options, args

def logargv():
    pid = os.getpid()
    logfile = datetime.now().strftime(f"/tmp/%y%m%d_%H%M%S%f_{pid}.args")
    with open(logfile,"w") as stream:
        pprint(sys.argv,stream=stream)

def logoptions(options,args):
    pid = os.getpid()
    logfile = datetime.now().strftime(f"/tmp/%y%m%d_%H%M%S%f_{pid}.opts")
    data = {
            "options": options.__dict__,
            "args": args
            }
    with open(logfile,"w") as stream:
        pprint(data,stream=stream)

def mythtv_data(endpoint, data = None):
    if not endpoint in endpoints:
        return None
    url = f"{api_url}{endpoints[endpoint]['path']}"
    if endpoints[endpoint]['type'] == 'GET':
        response = requests.get(url, 
                params=data, 
                headers={'Accept': 'application/json'})
    elif endpoints[endpoint]['type'] == 'POST':
        response = requests.post(url, 
                data=data, 
                headers={'Accept': 'application/json'})
    else:
        print(f"Invalid Endpoint: {endpoint}")
        return None
    if response.ok:
        return response.json()
    else:
        return None

def mythtv_encoders():
    el = mythtv_data('Encoders')
    response = None
    if 'EncoderList' in el:
        if 'Encoders' in el['EncoderList']:
            response = el['EncoderList']['Encoders']
    return response

if __name__ == "__main__":
    loadconfig()
    main()

