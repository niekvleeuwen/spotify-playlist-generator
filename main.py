# cli arguments
import sys
# web scrape
from bs4 import BeautifulSoup
import requests
# spotify
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from credentials import *

token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
spotify = spotipy.Spotify(auth=token)

def serialize(string):
    string = string.replace("'", "")
    string = string.split("/")
    string = string[0].split("(")
    return string[0]

def readItemsFromURL(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.find("tbody").find_all("tr")

def addItemsToSpotify(title, artist):
    result = spotify.search(q='artist:' + artist + ' track:' + title, type='track', limit=1)
    track = result['tracks']['items']
    
    # check if spotify API found a match for our query
    if track:
        print(title + " - " + artist + " - " + track[0]['id'])
        spotify.playlist_add_items(playlist_uri, [track[0]['id']])
    else:
        print(title + " - " + artist + " - FAILED! :(")

# get items from url
if len(sys.argv) > 1:
    rows = readItemsFromURL(sys.argv[1])
else:
    print("Error: no url given")
    exit()

# loop trough all the items
for row in rows:
    cells = row.find_all("td")
    number = cells[0].get_text()
    artist = serialize(cells[1].get_text())
    title = serialize(cells[2].get_text())
    addItemsToSpotify(title, artist)
    
