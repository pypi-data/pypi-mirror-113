#!/usr/bin/python

import json
import requests

response = requests.get("http://www.localhost:4040/api/tunnels")
json = response.json()
ip = json['tunnels'][0]['public_url']

ip = ip.replace("tcp://","")
print(ip)