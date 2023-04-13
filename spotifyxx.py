import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from json.decoder import JSONDecodeError

#get username from terminal
username = sys.argv[1]

#User ID = magicdawn89?si=f6577549ae7846b9

#erase cache and prompt for user permission

try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

#create out spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])