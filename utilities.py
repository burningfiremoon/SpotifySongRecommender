import time
from sklearn.cluster import KMeans
import joblib
import boto3
import mysql.connector
from mysql.connector.cursor import MySQLCursor
from enum import Enum

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

returns:
    True: if Track successfully set
    False: if Track already exist
======================="""
def set_track(cursor: MySQLCursor, song: Track) -> bool:
    # duplicate ID check
    if contain_track(cursor=cursor, track_id=song.track_id):
        return False
    
    # USE is similar to change director (cd)
    insert_query = """
        INSERT INTO tracks (track_id, song_name, artist_name)
        VALUES (%s, %s, %s)
    """
    values = (song.track_id, song.song_name, song.artist_name)

    cursor.execute(insert_query, values)
    # cursor.commit() # leave this to the caller? (better practice)
    
    return True

"""=======================
delete track from SQL database

returns:
    True: if Track is deleted
    False: if Track not found

======================="""
def delete_track(cursor: MySQLCursor, track_id: str) -> bool:
    # duplicate ID check
    if !contain_track(cursor=cursor, track_id=track_id):
        return False
    
    delete_query = """
        DELETE FROM tracks
        WHERE track_id = %s
    """
    cursor.execute(delete_query, (track_id,))
    return cursor.rowcount > 0 # returns True if something was deleted

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

