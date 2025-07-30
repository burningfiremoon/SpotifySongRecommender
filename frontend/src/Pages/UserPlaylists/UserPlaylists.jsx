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
            // console.log("All tracks:", allTracks)
            // Fetch to get song_id, tempo, loudness, energy, danceability, liveness, speechiness, acousticness, instrumentalness, valence

            // const idsParam = batch
            //     .filter((track) => track && track.id)
            //     .map(allTracks => allTracks.id)
            //     .join(',');


            // Current steps to program:
            /* 
            1. spotify id -> raccobeat id
                /v1/track?ids=4ogUNsrAiv68W9LnD6mJJm,3gPYoFtn70aTgl546XVSET
                1 - 40
            2. Take Raccobeat id
            3. get audio features
                /v1/track/367e626c-6661-42df-9709-321ebea2403d/audio-features'
            4. send it to the backend
            */
            // translate spotify id -> raccobeat id
            // doing for 20 random songs
            const getRandomTracks = (allTracks) => {
                const shuffled = [...allTracks].sort(() => 0.5 - Math.random()).filter((track) => track && track.id);
                return shuffled.slice(0, 20);
            }

            async function fetchAudioFeatures(ids) {
                const audioFeatures = [];

                for (const id of ids){
                    try {
                        const config = {
                            method: 'get',
                            maxBodyLength: Infinity,
                            url: `https://api.reccobeats.com/v1/track/${id}/audio-features`,
                            headers: {
                                'Accept': 'application/json'
                            }
                        };

                        const response = await axios.request(config);

                        audioFeatures.push({id,data: response.data });
                    } catch (error){
                        console.error(`Failed to fetch audio features`, error);
                    }
                }
                return audioFeatures;
            }

            const random20 = getRandomTracks(allTracks);

            const idParam = random20.map(track => track.id).join(',');
            console.log(idParam);
            let config = {
                method: 'get',
                maxBodyLength: Infinity,
                url: `https://api.reccobeats.com/v1/track?ids=${idParam}`,
                headers: {
                    'Accept': 'application/json'
                }
            };

            const response = await axios.request(config);

            const ids = response.data.content.map(track => track.id);
            console.log("This is ids:",ids);

            const audioFeatures = await fetchAudioFeatures(ids);
            console.log("Audio features: ", audioFeatures);

            const reccomendedSongs = await fetch("http://127.0.0.1:5000/generate",{
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    listOfSongs: audioFeatures,
                    token: token,
                }),
            });

            const data = await reccomendedSongs.json()
            console.log(data)

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