import React from 'react';
import LoginButton from './LoginButton';
import bassClefLogo from '../../assets/SongRecommenderIcon.png';
import './HomeScreen.css';

const HomeScreen = () => {
  return (
    <div className='homepage'>
        {/*Top bar */}
        <div className='homepage_topbar'>
            <img src={bassClefLogo} alt="Logo" className='homepage_logo'/>
            <span className='homepage_brand'>CHARLES & JAD</span>
        </div>

        {/* Main content */}
        <div className="homepage_content">
            <h1 className="homepage_title">Spotify Song <br />Recommender</h1>
            <div className='homepage_subtitleAndButton'>
                <p className="homepage_subtitle">Update your playlists with similar songs</p>
                <div className="homepage_button"><LoginButton/></div>
            </div>
        </div>
    </div>
  );
}

export default HomeScreen