import React from 'react'
import { useEffect, useState } from 'react'
import './UserPlaylists.css'
import ButtonLink from '../../Componenets/ButtonLink';
import { Route } from 'react-router-dom';

function UserPlaylists() {
    const [playlists, setPlaylists] = useState([]);
    const [selectedPlaylists, setSelectedPlaylists] = useState([]);
    const [token, setToken] = useState("");
    const [tracks, setTracks] = useState([]);

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

    const generateJson = async (playlists, _token = token) => {

        // All song Ids and popularity is generated and stored
        try {
            const allTracks = await Promise.all(
                playlists.map(async (playlist) =>{
                    const res = await fetch(
                        `https://api.spotify.com/v1/playlists/${playlist.id}/tracks?fields=total,limit,offset,items(track(id,popularity))`,
                        {headers:{
                            Authorization: `Bearer ${_token}`,
                        },
                    }
                    );
                    const data = await res.json();
                    return {
                        tracks: data.items.map((item) => item.track),
                    };
                })
            );
            console.log("All tracks:", allTracks)
        } catch (err){
            console.error("Error generating playlist JSON:", err);
        };
        
        // Fetch to get song_id, tempo, loudness, energy, danceability, liveness, speechiness, acousticness, instrumentalness, valence
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
                        <p>{playlist.id}</p>
                        <button onClick={() => unselectPlaylist(playlist)}>Minus Button</button>
                    </li>
                ))}
            </ul>
        </div>
        <ButtonLink route={'/loading'} onClick={() => generateJson(selectedPlaylists)}>Generate</ButtonLink>
    </>
  );
}

export default UserPlaylists