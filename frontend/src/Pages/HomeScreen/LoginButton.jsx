// src/LoginButton.jsx
import React from 'react';

const CLIENT_ID = 'd78014048e58437f8e61b35c08263634'; // replace this with real value
const REDIRECT_URI = 'http://127.0.0.1:5173/callback';
const SCOPE = 'user-read-private user-read-email';

export default function LoginButton() {
  const handleLogin = () => {
    if (!CLIENT_ID) {
      console.error('❌ CLIENT_ID is missing!');
      return;
    }

    const authUrl = `https://accounts.spotify.com/authorize` +
      `?response_type=code` +
      `&client_id=${encodeURIComponent(CLIENT_ID)}` +
      `&redirect_uri=${encodeURIComponent(REDIRECT_URI)}` +
      `&scope=${encodeURIComponent(SCOPE)}`;

    console.log('🔗 Redirecting to Spotify:', authUrl); // ✅ LOG before redirect

    window.location.href = authUrl;
  };

  return <button onClick={handleLogin}>Login With Spotify</button>;
}