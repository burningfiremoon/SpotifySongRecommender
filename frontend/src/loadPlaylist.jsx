import {React, useEffect, useState} from 'react'

function LoadPlaylist({token}) {
  const [tracks, setTracks] = useState([]);
  const [trackIds, setTrackIds] = useState([]);

  useEffect(() =>{
    fetch("../public/first_100_songs_2.json")
    .then((res) => res.json())
    .then((data) => {
      setTrackIds(data);
    })
    .catch((err) => console.error("Didn't load songIDs: ", err));
  }, []);


  // Extraction
  useEffect(() => {
    if (trackIds.length === 0 || !token) return;

    const ids = trackIds.map((song) => song.id); // this extracts just ids
    const idsParam = ids.slice(0, 49).join(","); // joins them together

    fetch(`https://api.spotify.com/v1/tracks?ids=${idsParam}`,{
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    .then((res) => res.json())
    .then((data) => setTracks(data.tracks))
    .catch((err) => console.error("Spotify API error:", err));
  }, [trackIds, token]);

  return (
    <div>
      <h2>Loaded Tracks</h2>
      {tracks.length === 0 ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {tracks.map((track) =>(
            <li key={track.id}>
              <strong>{track.name}</strong> by {track.artists.map(a => a.name).join(", ")}
              <br/>
              <img src={track.album.images[0]?.url} alt="Album cover" width={100}/>

            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default LoadPlaylist