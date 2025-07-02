from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

app = Flask(__name__)
CORS(app) # Allow requests from React dev server

CLIENT_ID = os.getenv('JADCLIENT_ID')
CLIENT_SECRET = os.getenv('JADCLIENT_SECRET')
REDIRECT_URI = "http://127.0.0.1:5173/callback"
MLFLOW_TRACKING_URI="http://ec2-3-148-231-10.us-east-2.compute.amazonaws.com:5000/"

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
    data = request.get_json()
    


if __name__ == "__main__":
    app.run(port=5000, debug=True)
