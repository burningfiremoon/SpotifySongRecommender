import React from 'react'
import { useEffect, useState } from 'react'
import './UserPlaylists.css'
import ButtonLink from '../../Componenets/ButtonLink';
import { Route } from 'react-router-dom';
import axios from 'axios';

function UserPlaylists() {
    const [playlists, setPlaylists] = useState([]);
    const [selectedPlaylists, setSelectedPlaylists] = useState([]);
    const [token, setToken] = useState("");

    // Getting token this might need to be async
    useEffect(() => {
        const storedToken = sessionStorage.getItem("spotify_access_token");

        if (storedToken) {
            setToken(storedToken);
        } else {
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

    const sendJsonToBackend = async (data) => {
        try {
            const response = await fetch('http://127.0.0.1:5000/generate',{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();
            console.log('Server response: ', result);
        } catch (err){
            console.log('Error sending JSON', err);
        }
    }

    const generateJson = async (playlists) => {
        const batchSize = 2;

        // All song Ids and popularity is generated and stored
        try {
            const allTracks = (await Promise.all(
                playlists.map(async (playlist) =>{
                    const res = await fetch(
                        `https://api.spotify.com/v1/playlists/${playlist.id}/tracks?fields=total,limit,offset,items(track(id,popularity))`,
                        {headers:{
                            Authorization: `Bearer ${token}`,
                        },
                    }
                    );
                    const data = await res.json();
                    return data.items.map((item) => item.track);
                })
            )).flat();
            console.log("All tracks:", allTracks)
            // Fetch to get song_id, tempo, loudness, energy, danceability, liveness, speechiness, acousticness, instrumentalness, valence

            // const idsParam = batch
            //     .filter((track) => track && track.id)
            //     .map(allTracks => allTracks.id)
            //     .join(',');

            const batch = allTracks
                .slice(1, 10)
                .filter((track) => track && track.id);
                console.log("This is batch:", batch)
            

            let config = {
                method: 'get',
                maxBodyLength: Infinity,
                url: 'https://api.reccobeats.com/v1/track?ids=8c438304-e436-43ea-9fe6-5e17199c2dfd',
                headers: { 
                    'Accept': 'application/json'
                }
            };

            axios.request(config)
            .then((response) => {
            console.log(JSON.stringify(response.data));
            })
            .catch((error) => {
            console.log(error);
            });
            // const allAudioFeatures = async (allTracks) => {
            //     let allFeatures = [];
            //     try{
            //         for (const track of batch){
            //             console.log(track.id);
            //             const config = {
            //                 method: 'get',
            //                 maxBodyLength: Infinity,
            //                 url: `https://api.reccobeats.com/v1/track/${track.id}/audio-features`,
            //                 headers: {
            //                     'Accept': 'application/json'
            //                 }
            //             };
            //             const res = await axios.request(config);
            //             console.log(`Features for ${track.id}`, res.data);

            //             allFeatures.push({
            //                 id: track.id,
            //                 ...res.data
            //             })
            //         }

            //     } catch (err) {
            //         console.error('Error fetching:', err)
            //     }
            //     console.log("All Features:", allFeatures);
            //     return allFeatures
            // } 

            // allAudioFeatures(allTracks).then(features => {
            //     console.log("Features:", features);
            //     sendJsonToBackend(allAudioFeatures);
            // })

        } catch (err){
            console.error("Error generating playlist JSON:", err);
        };

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