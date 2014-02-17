#!/usr/bin/python

import urllib, urllib2, StringIO, json

def coordinates( address ):
    urlParams = { 'address': address, 'sensor': 'false', }
    url = 'http://maps.google.com/maps/api/geocode/json?' + urllib.urlencode( urlParams )
    response = urllib2.urlopen( url )
    responseBody = response.read()

    body = StringIO.StringIO( responseBody )
    result = json.load( body )
    if 'status' not in result or result['status'] != 'OK':
        return None
    else:
        return {
            'lat': result['results'][0]['geometry']['location']['lat'],
            'lng': result['results'][0]['geometry']['location']['lng']
        }

print coordinates("136 102nd Ave SE Bellevue WA 98004")
