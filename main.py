from flask import Flask, request, redirect, session, url_for
import os
from dotenv import load_dotenv
load_dotenv()
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth 
from spotipy.cache_handler import FlaskSessionCacheHandler
import utilities

#pandas imports
import pandas as pd

tempi = 575000

# songData = pd.read_csv(f"models/tracks_features.csv")
songData = pd.read_csv(f"models/songData_{str(tempi/100000)}")
songIDs = songData['id'] # name is not needed

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
    i = tempi
    get_token()

    BATCHSIZE = 100000


    # Start of mini test ==============================================
    testBatchSize = 15000
    z = 0
    workingFrame = songIDs[i:i+testBatchSize]

    # 100000 at a time
    for j in range(0, testBatchSize, 50):
        batchIDs = workingFrame[j:j+50]
        tracks = getTracks(batchIDs)
        for track in tracks:
            songData.loc[songData['id'] == track['id'], 'popularity'] = track['popularity']
            songData.loc[songData['id'] == track['id'], 'name'] = track['name']
            z += 1

    # save songData
    i += testBatchSize
    print(f"Done Batch {i/100000}")
    print(f"this is i: {i}\n")
    print(f"this is z: {z}")
    utilities.dump_to_csv(fileName=(f"songData_{str(i/100000)}"), df=songData)
    # End of mini test ==============================================

    # while ((i+BATCHSIZE) <= songIDs.shape[0]):
    #     get_token()
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
    #     i += BATCHSIZE
    #     print(f"Done Batch {i/100000}")
    #     utilities.dump_to_csv(fileName=(f"songData_{str(i/100000)}"), df=songData)
    
    # # Start of last 4025
    # print("starting last 4025")

    # for j in range(0, 4000-50, 50):
    #     batchIDs = songIDs[j:j+50]
    #     tracks = getTracks(batchIDs)
    #     for track in tracks:
    #         songData.loc[songData['id'] == track['id'], 'popularity'] = track['popularity']
    #         songData.loc[songData['id'] == track['id'], 'name'] = track['name']

    # # save songData
    # i += 4000
    # utilities.dump_to_csv(fileName=(f"songData_{str(i/100000)}"), df=songData)

    # print("last 25")

    # batchIDs = songIDs[i:i+25]
    # tracks = getTracks(batchIDs)
    # for track in tracks:
    #     songData.loc[songData['id'] == track['id'], 'popularity'] = track['popularity']
    #     songData.loc[songData['id'] == track['id'], 'name'] = track['name']

    # # save songData
    # i += 25
    # utilities.dump_to_csv(fileName=(f"songData_{str(i/100000)}"), df=songData)

    return 'FINISHED'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)