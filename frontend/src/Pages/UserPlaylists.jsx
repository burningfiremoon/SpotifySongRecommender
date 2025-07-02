import React from 'react'
import { useEffect, useState } from 'react'

function UserPlaylists() {
    const [playlists, setPlaylists] = useState([]);
    const [userID, setUserID] = useState([]);
    const [token, setToken] = useState("");

    // Getting token
    useEffect(() => {
        console.log("Getting token");
        const storedToken = sessionStorage.getItem("spotify_access_token");

        if (storedToken) {
            setToken(storedToken);
        } else {
            console.log("No token found");
            return(<p>No token found</p>)
        }
    }, []);

    // Getting user's information
    useEffect(() =>{
        if(!token) return;
        fetch('https://api.spotify.com/v1/me',{
            headers:{
                Authorization: `Bearer ${token}`,
            },
        })
        .then((res) => res.json())
        .then((data) => setUserID(data.id))
        .catch((err) => console.error("Spotify API error:", err)); // this doesn't catch spotify error, need to redo
    }, [token]);

    // Getting user's playlists
    useEffect(() =>{
        console.log(`This is userID: ${userID}`)
        fetch(`https://api.spotify.com/v1/users/${userID}/playlists`,{
            headers:{
                Authorization: `Bearer ${token}`,
            },
        })
        .then((res) => res.json())
        .then((data) => setPlaylists(data.items));
    },[userID, token]);

  return (
    <>
        <h2>Loaded Playlists</h2>
        {playlists.length === 0 ? (
            <p>Loading...</p>
        ) : (
            <ul>
                {playlists.map((playlist)=>(
                    <li key={playlist.id}>
                        <strong>{playlist.name}</strong>
                    </li>
                ))}
            </ul>
        )}
    </>
  );
}

export default UserPlaylists