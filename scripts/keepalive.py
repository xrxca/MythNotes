#!/usr/bin/python3
import requests
from syslog import openlog, syslog

api_url = 'http://localhost:6744/'
iplist = {
    1: '192.168.1.129',
    2: '192.168.1.128'
    }

endpoints = {
        'Encoders': {
            'type': 'GET',
            'path': 'Dvr/GetEncoderList'
            }
        }

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

openlog(ident="MythTV")
el = mythtv_data('Encoders')
for e in el['EncoderList']['Encoders']:
    if e['State'] == 7:
        id = e['Id'];
        title = "";
        if "Recording" in e:
            if "Title" in e['Recording']:
                title = e['Recording']['Title']
        url = f"http://{iplist[id]}/key/D"
        r = requests.get(url)
        syslog(f"KeepAlive: HDPVR{id} {title}")
