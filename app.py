from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import urllib.parse
import mlflow
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
from sklearn.pipeline import Pipeline
load_dotenv()

app = Flask(__name__)
CORS(app) # Allow requests from React dev server

CLIENT_ID = os.getenv('JADCLIENT_ID')
CLIENT_SECRET = os.getenv('JADCLIENT_SECRET')
# CLIENT_ID = os.getenv('CHARLESCLIENT_ID')
# CLIENT_SECRET = os.getenv('CHARLESCLIENT_SECRET')
REDIRECT_URI = "http://127.0.0.1:5173/callback"
MLFLOW_TRACKING_URI="http://ec2-3-148-231-10.us-east-2.compute.amazonaws.com:5000/"
LATEST_MINIBATCH_KMEANS_MODEL = '280ab65dc8e0410ab88d110d5b010100'

@app.route("/")
def home():
    return "Flask backend is Running"

@app.route("/api/exchange_token", methods=['POST'])
def exchange_token():
    data = request.get_json()
    code = data.get("code")

    if not code:
        return jsonify({"error": "Missing authorization code"}), 400

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post("https://accounts.spotify.com/api/token", data=urllib.parse.urlencode(payload), headers=headers)

    print("Spotify response status:", response.status_code)
    print("Spotify response body:", response.text)

    if response.status_code != 200:
        return jsonify({"error": "Failed to get access token", "details": response.json()}), 500
    
    return jsonify(response.json())

@app.route("/generate", methods=['POST'])
def generate_playlist():
    try:
        # Get data from frontend
        data = request.get_json()
        if not data:
            return jsonify({"error": "No Data Provided"}), 400
        
        token = data.get("token")
        
        # Convert JSON to data frame
        df = pd.DataFrame(data)
        features = [
            'tempo', 'loudness', 'energy', 'danceability', 'liveness',
            'speechiness', 'acousticness', 'instrumentalness', 'valence'
        ]
        X = df[features]

        # Load model from MLflow
        model = get_latest_model()

        # Average the features of user's songs
        X_average = X.mean().to_frame().T

        cluster_index = int(model.predict(X_average)[0])

        # mySQL
        SQLid = os.getenv("SQL_ID")
        SQLpassword = os.getenv("SQL_PASSWORD")

        try:
            cnx = mysql.connector.connect(
            user = SQLid,
            password = SQLpassword,
            host = 'trackdatabase.cfgs6eaksjht.ca-central-1.rds.amazonaws.com',
            database = 'Tracks_Database',
            port = 3306
        )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                jsonify({"error": "Something is wrong with user name and password"}), 500
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                jsonify({"error": "database doesn't exist"}), 500
            else:
                jsonify({"error": str(err)}), 500

        mycursor = cnx.cursor()

        mycursor.execute(
            """
            SELECT track_id FROM songs
            WHERE cluster_id = %s
            ORDER BY RAND()
            LIMIT 500
            """,
            (cluster_index,)
        )
        candidate_ids = [row[0] for row in mycursor.fetchall()] # List of IDs

        popular_tracks = []
        for track_id in candidate_ids:
            popularity = get_spotify_popularity(track_id, token)
            if popularity > 75:
                popular_tracks.append(track_id)
            if len(popular_tracks) == 50:
                break

        return popular_tracks.json(), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_spotify_popularity(track_id, token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {
            "Authoriation": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("popularity", 0) # returns popularity of 0 if it cant be found
    else:
        return 0

def get_latest_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    model_uri = "runs:/{LATEST_MINIBATCH_KMEANS_MODEL}/minibatch_kmeans_model"
    return mlflow.sklearn.load_model(model_uri)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
