#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 23:30:15 2021

@author: hakanbernhardsson
"""
#Läs in variabler från Variables.txt
def get_pair(line):
    key, sep, value = line.strip().partition("=")
    return key, value

with open("../Variables.txt") as fd:
    var_list = dict(get_pair(line) for line in fd)


api_key=var_list["google_maps_api_token"]

#Utanför Halmstad
start_lat=56.673286
start_long=12.899419

#McD Helsingborg
end_lat=56.044640
end_long=12.694479

import json
import requests

def decode_polyline(polyline_str):
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so just keep
    # track of whether we've hit the end of the string. In each
    # while loop iteration, a single coordinate is decoded.
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dictionary to apply them later
        for unit in ['latitude', 'longitude']:
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index+=1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']

        coordinates.append((lat / 100000.0, lng / 100000.0))

    return coordinates

call_url="https://maps.googleapis.com/maps/api/directions/json?origin="+str(start_lat)+","+str(start_long)+"&destination="+str(end_lat)+","+str(end_long)+"&key="+api_key

response = requests.get(call_url)
response_json = json.loads(response.text)

response_polyline=decode_polyline(response_json["routes"][0]["overview_polyline"]["points"])

def create_streetview_url(lat, long):
    urlString="https://maps.googleapis.com/maps/api/streetview?size=640x640&location="+str(lat)+","+str(long)+"&key="+api_key
    return urlString

def goodify_filename(number):
    filename=""
    if int( number/10  )==0:
        filename="00"+str(number)+".jpg"
    elif int( number/10)==1:
        filename="0"+str(number)+".jpg"
    else:
        filename=str(number)+".jpg"
    return filename

for i in range(len(response_polyline)):
    tempLat=response_polyline[i][0]
    tempLong=response_polyline[i][1]
    response=requests.get( create_streetview_url(tempLat, tempLong) )
    if response.status_code == 200:
        with open(goodify_filename(i), 'wb') as f:
            f.write(response.content)
