import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import LoginButton from './LoginButton'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import Callback from './Callback'
import CreatePlaylist from './Pages/CreatePlaylist'
import UserPlaylists from './Pages/UserPlaylists/UserPlaylists'

function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<LoginButton/>}/>
          <Route path='/callback' element={<Callback/>} />
          <Route path="/playlist" element={<CreatePlaylist/>}/>
          <Route path="/UserPlaylists" element={<UserPlaylists/>}/>
        </Routes>
      </Router>
    </>
  )
}

export default App
