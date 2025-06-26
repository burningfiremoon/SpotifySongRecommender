import React from 'react'
import { useState, useEffect } from 'react'
import LoadPlaylist from '../loadPlaylist'

function Playlist() {
    const [token, setToken] = useState("");

    useEffect(() => {
        console.log("Getting token");
        const storedToken = localStorage.getItem("spotify_access_token");

        if (storedToken) {
            setToken(storedToken);
        } else {
            console.log("No token found");
            return(<p>No token found</p>)
        }
    }, []);

  return (
    <div>
        <h3>Loading playlist</h3>
        <LoadPlaylist token={token}/>
    </div>

  )
}

export default Playlist