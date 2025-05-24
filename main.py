from flask import Flask, request, redirect, session, url_for
import os
from dotenv import load_dotenv
load_dotenv()
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth 
from spotipy.cache_handler import FlaskSessionCacheHandler

#pandas imports
import pandas as pd

songData = pd.read_csv('models/tracks_features.csv')
songIDs = songData['id'] # name is not needed
songData['popularity'] = None

# End of pandas

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

app = Flask(__name__)

app.config['SECRET_KEY']= os.urandom(64)

cache_handler = FlaskSessionCacheHandler(session)

# authentication manager
sp_oauth = SpotifyOAuth(
    client_id = client_id,
    client_secret = client_secret,
    redirect_uri = redirect_uri,
    cache_handler = cache_handler,
    show_dialog=True
)


def get_token():
    # if user is not logged in
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return None

def getTracks(_songIDs: [str]) -> [{}]:
    get_token()
    
    songs = sp.tracks(tracks=_songIDs)
    songs_data = []

    for track in songs['tracks']:
        song_info = {
            'name': track['name'],
            'id': track['id'],
            'popularity': track['popularity']
        }
        songs_data.append(song_info)

    return songs_data


sp = Spotify(auth_manager=sp_oauth)

@app.route('/')
def home():
    # if user is not logged in
    get_token()
    return redirect(url_for('get_features'))

# creating end-point to refresh expired token
# user doesn't have to re log-in
# unless additional scopes are needed
@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_features'))

@app.route('/get_features')
def get_features():
    i = 0

    BATCHSIZE = 100000

    # while ((i+BATCHSIZE) <= songIDs.shape[0]):
    #     # df.loc[df['Name'] == 'Bob', 'Age'] = 31

    #     # Take 100000 of songData
    #     workingFrame = songIDs[i:i+BATCHSIZE]

    #     # 100000 at a time
    #     for j in range(0, BATCHSIZE-50, 50):
    #         batchIDs = songIDs[j:j+50]
    #         tracks = getTracks(batchIDs)
    #         for track in tracks:
    #             songData.loc[songData['id'] == track['id'], 'popularity'] = track['popularity']
    #             songData.loc[songData['id'] == track['id'], 'name'] = track['name']

    #     # save songData

    # Start of test ===============

    workingFrame = songIDs[i:i+100]

    for j in range(0, 100, 50):
        batchIDs = songIDs[j:j+50]
        print(f"This is j: {j}")
        print(batchIDs)
        tracks = getTracks(batchIDs)
        for track in tracks:
            songData.loc[songData['id'] == track['id'], 'popularity'] = track['popularity']
            songData.loc[songData['id'] == track['id'], 'name'] = track['name']
            print(f"{track['name']}: {track['popularity']}")

    # save songData
    songData.head(50)

    # End of test ========================
    return

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)