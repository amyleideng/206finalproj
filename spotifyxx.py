import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util

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
