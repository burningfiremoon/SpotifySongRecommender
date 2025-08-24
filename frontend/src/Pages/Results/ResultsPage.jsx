import { useState, useEffect } from "react"
import Button from "../../Componenets/Button";
import { useNavigate } from "react-router-dom";


function ResultsPage() {
    const [trackDetails, setTrackDetails] = useState([])
    const navigate = useNavigate()
    useEffect(() => {
        const saved = sessionStorage.getItem("trackDetails")
        if (saved) {
            setTrackDetails(JSON.parse(saved))
        }
    }, []);

    return (
        <div>
            <h2>Generated Songs</h2>
            <ul>
                {trackDetails.map((track) => (
                    <li key={track.id}>
                        {track?.album?.images?.[0]?.url ? (
                            <div>
                                <img src={track.album.images[0].url} alt="Album Cover" width={60} />
                                <p><strong>{track.name}</strong> by {track.artists.map((artist) => artist.name).join(", ")}</p>
                            </div>
                        ) : (
                            <p>No image available</p>
                        )}
                    </li>
                ))}
            </ul>
            <button onClick={() => (navigate("/UserPlaylists"))}> Back </button>
        </div>
    )
}

export default ResultsPage