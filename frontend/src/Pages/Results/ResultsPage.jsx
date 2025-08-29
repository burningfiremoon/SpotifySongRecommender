import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import "./ResultsPage.css";

function ResultsPage() {
  const [trackDetails, setTrackDetails] = useState([])
  const [selectedTracks, setSelectedTracks] = useState([])
  const navigate = useNavigate()
  
  useEffect(() => {
    const saved = sessionStorage.getItem("trackDetails")
    if (saved) {
      setTrackDetails(JSON.parse(saved))
    }
  }, [])

  const handleCheckboxChange = (trackId) => {
    setSelectedTracks((prev) =>
      prev.includes(trackId)
        ? prev.filter((id) => id !== trackId) // uncheck → remove
        : [...prev, trackId] // check → add
    );
  };

  return (
    <>
        <div>
            <h2>Generated Songs</h2>
            <div className="ResultsContainer">
            <ul>
                {trackDetails.map((track) => (
                    <li key={track.id} className="track-item">
                        {track?.album?.images?.[0]?.url ? (
                            <div className="track-content">
                                <input
                                    type="checkbox"
                                    checked={selectedTracks.includes(track.id)}
                                    onChange={() => (handleCheckboxChange(track.id))}
                                />
                                <img src={track.album.images[0].url} alt="Album Cover" width={60} />
                                <div className="track-info">
                                    <p className="track-name"><strong>{track.name}</strong></p>
                                    <p className="track-artists">
                                        {track.artists.slice(0, 3).map((artist) => artist.name).join(", ")}
                                    </p>
                                </div>
                            </div>
                        ): (
                            <p>No image available</p>
                        )}

                    </li>
                ))}
            </ul>
            </div>
            <button onClick={() => (navigate("/UserPlaylists"))}> Back </button>
        </div>
        <div style={{ marginTop: "1rem", color: "white" }}>
            <strong>Selected Track IDs:</strong> {selectedTracks.join(", ")}
        </div>
    </>
  )
}

export default ResultsPage
