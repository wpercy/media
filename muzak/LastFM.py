"""
A module for interacting with the LastFM API

check for error in response by checking >> if "error" in r.json()
"""

import requests

KEY = '84c9195402838510b5a4a85c708c9678'
URL = 'http:////ws.audioscrobbler.com/2.0/'

def get_track_info(name, artist):
    r = requests.get("%s?method=track.getInfo&format=json&track=%s&artist=%s&api_key=%s" % (URL,name,artist,KEY))
    album_title = r.json()['track']['album']['title']
    return r.json()

def get_album_info(name, artist):
    r = requests.get("%s?method=album.getInfo&format=json&album=%s&artist=%s&api_key=%s" % (URL,name,artist,KEY))
    num_tracks = len(r.json()['album']['tracks']['track'])
    year_released = r.json()['album']['releasedate'].strip().split()[2].strip(',')
    tags = [ t['name'] for t in r.json()['album']['toptags']['tag'] ]
    return r.json()

