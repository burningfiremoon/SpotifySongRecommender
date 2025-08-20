import webbrowser, hashlib, random, utilities, os, requests, mlflow, pandas as pd, mysql.connector, urllib.parse, base64
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from http.server import HTTPServer, BaseHTTPRequestHandler
load_dotenv()

# Global variables
ACCESS_TOKEN = None
AUTH_CODE = None

# HTTP server to get code
class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global AUTH_CODE
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "code" in params:
            AUTH_CODE = params["code"][0]
            self.send_response(200)
            self.send_header("Context-type", "text/html")
            self.end_headers()
            self.wfile.write(b"You may close this window.")
        else:
            self.send_response(400)
            self.end_headers()

def generateCodeVerifier(length: int):
    text = ''
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    for i in range(length):
        text += possible[random.randint(0, len(possible)-1)]
    
    return text

def generateCodeChallenge(codeVerifier: str):
    # SHA-256 hash of the verifier (bytes)
    digest = hashlib.sha256(codeVerifier.encode("utf-8")).digest()

    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")    

def redirectToAuthCodeFlow(client_id: str, redirect_uri: str, verifier: str):
    challenge = generateCodeChallenge(verifier)
    
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "user-read-private user-read-email",
        "code_challenge_method": "S256",
        "code_challenge": challenge
    }
    url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"
    webbrowser.open(url)

def requestAccessToken(client_id: str, code: str, verifier: str, redirect_uri):
    global ACCESS_TOKEN

    url = "https://accounts.spotify.com/api/token"
    data = {
        "client_id": client_id,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": verifier
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Token request failed: {response.status_code},{response.text}")
    
    tokenInfo = response.json()
    print(tokenInfo)
    ACCESS_TOKEN = tokenInfo["access_token"]

    return tokenInfo

if __name__ == '__main__':
    CLIENT_ID = os.getenv('JADCLIENT_ID')
    CLIENT_SECRET = os.getenv('JADCLIENT_SECRET')
    REDIRECT_URI = "http://127.0.0.1:5173/callback"
    VERIFIER = generateCodeVerifier(128)
    # starts the local server to catch redirect
    server = HTTPServer(("127.0.0.1", 5173), RedirectHandler)

    import threading
    threading.Thread(target=server.serve_forever, daemon=True).start()

    # Spotify login
    redirectToAuthCodeFlow(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI, verifier=VERIFIER)

    print("Authorization")
    # How do you async python?
    import time
    while AUTH_CODE is None:
        time.sleep(1)
    
    server.shutdown()

    requestAccessToken(client_id=CLIENT_ID, code=AUTH_CODE, redirect_uri=REDIRECT_URI, verifier=VERIFIER)
    # after here we have access token in ACCESS_TOKEN
    print("We made it")


    

