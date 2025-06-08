import time
from sklearn.cluster import KMeans
import joblib
import boto3
import mysql.connector
from mysql.connector.cursor import MySQLCursor

class Track:
    track_id:str
    song_name:str
    artist_name:str
    def __init__(self, track_id: str, song_name: str, artist_name: str):
        self.track_id = track_id
        self.song_name = song_name
        self.artist_name = artist_name


def generate_file_name(model: KMeans, directory: str = "./models") -> str:
    timeStamp = time.strftime("%Y%m%d-%H%M")
    modelName = type(model).__name__
    return f"{directory}/{modelName}_{timeStamp}"


def dump_model(model: KMeans) -> str:
    fileName = generate_file_name(model)
    joblib.dump(model, fileName)
    return fileName


def load_model(directory: str) -> KMeans:
    return joblib.load(directory)

# SQL FUNCTION

"""=======================
searches for Track using track_id

returns bool value

======================="""
def contain_track(cursor: MySQLCursor, track_id: str) -> bool:
    pass

"""=======================
sets Track to sql database

======================="""
def set_track(cursor: MySQLCursor, song: Track):
    pass

"""=======================
delete track from SQL database

returns:
    True: if Track is deleted
    False: if Track not found

======================="""
def delete_track(cursor: MySQLCursor, track_id: str) -> bool:
    pass

"""=======================
gets a Track from database

returns Track

======================="""
def get_track(cursor: MySQLCursor, track_id:str) -> Track:
    pass

"""=======================
edits song_name 

======================="""
def edit_track(cursor: MySQLCursor, track_id: str, artist_name: str = None, song_name: str = None):
    pass

