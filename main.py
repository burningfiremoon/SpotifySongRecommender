from flask import Flask, request, redirect, session, url_for
import os
from dotenv import load_dotenv
load_dotenv()
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth 
from spotipy.cache_handler import FlaskSessionCacheHandler

#pandas imports
import pandas as pd

song_data = pd.read_csv('models/tracks_features.csv')

songIDs = song_data[['id', 'name']]

testSongs = [
    '7lmeHLHBe4nmXzuXc0HDjk',
    '1wsRitfRRtWyEapl0q22o8',
    '1hR0fIFK2qRG3f3RF70pb7',
    '2lbASgTSoDO7MTuLAXlTW0',
    '1MQTmpYOZ6fcMQc56Hdo7T'
    ]

testSongNames = [
    'Testify',
    'Guerrilla Radio',
    'Calm Like a Bomb',
    'Mic Check',
    'Sleep Now In the Fire'
]


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

# get playlist example
@app.route('/get_playlists')
def get_playlists():
    get_token()

    playlists = sp.current_user_playlists()
    playlists_info = [(pl['name'], pl['external_urls']['spotify']) for pl in playlists['items']]
    playlists_html = '<br>'.join([f'{name}: {url}' for name, url in playlists_info])

    return playlists_html

@app.route('/get_features')
def get_features():
    get_token()

    songs = sp.tracks(tracks=testSongs)
    songs_data = []

    for track in songs['tracks']:
        song_info = {
            'name': track['name'],
            'id': track['id'],
            'popularity': track['popularity']
        }
        songs_data.append(song_info)
    
    print(len(songs_data))

    songs_html = '<br>'.join([f'popularity: {track["popularity"]} {track["name"]}: {track["id"]}' for track in songs_data])

    return songs_html

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)