from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

app = Flask(__name__)
CORS(app) # Allow requests from React dev server

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = "http://127.0.0.1:5173/callback"

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


if __name__ == "__main__":
    app.run(port=5000, debug=True)
