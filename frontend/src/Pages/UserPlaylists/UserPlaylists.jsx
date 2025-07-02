import React from 'react'
import { useEffect, useState } from 'react'
import './UserPlaylists.css'

function UserPlaylists() {
    const [playlists, setPlaylists] = useState([]);
    const [selectedPlaylists, setSelectedPlaylists] = useState([]);
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

    // Getting user's playlists
    useEffect(() =>{
        if(!token){
            console.log("no Token");
            return;
        }
        fetch(`https://api.spotify.com/v1/me/playlists?limit=50`,{
            headers:{
                Authorization: `Bearer ${token}`,
            },
        })
        .then((res) => res.json())
        .then((data) => setPlaylists(data.items));
    }, [token]);

    const selectPlaylist = (playlist) =>{
        setPlaylists(playlists.filter(p => p.id !== playlist.id));
        setSelectedPlaylists([...selectedPlaylists, playlist]);
    }

    const unselectPlaylist = (playlist) =>{
        setSelectedPlaylists(selectedPlaylists.filter(p => p.id !== playlist.id));
        setPlaylists([...playlists, playlist]);
    }

  return (
    <>
        <h2>Loaded Playlists</h2>
        <div>
            <ul>
                {playlists.map((playlist)=>(
                    <li key={playlist.id}>
                        <strong>{playlist.name}</strong>
                        <button onClick={() => selectPlaylist(playlist)}>Add Button</button>
                    </li>
                ))}
            </ul>
            <ul>
                {selectedPlaylists.map((playlist)=>(
                    <li key={playlist.id}>
                        <strong>{playlist.name}</strong>
                        <button onClick={() => unselectPlaylist(playlist)}>Minus Button</button>
                    </li>
                ))}
            </ul>
        </div>
    </>
  );
}

export default UserPlaylists