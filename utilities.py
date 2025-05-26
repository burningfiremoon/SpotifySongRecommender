import time
from sklearn.cluster import KMeans
import joblib
import os
import requests
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

redirect_uri = "https://localhost:8888/callback"

clientID = os.getenv('CLIENT_ID')
clientSecret = os.getenv('CLIENT_SECRET')

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

def get_track_popularity(track_id: str) -> int:
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

def dump_to_csv(fileName, df):
    df.to_csv(f"models\{fileName}", index=False)

def dump_to_csv(fileName, df):
    df.to_csv(f"models\{fileName}", index=False)