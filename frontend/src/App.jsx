import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import LoginButton from './Pages/HomeScreen/LoginButton'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import Callback from './Callback'
import CreatePlaylist from './Pages/CreatePlaylist'
import UserPlaylists from './Pages/UserPlaylists/UserPlaylists'
import Loading from './Pages/Loading'
import HomeScreen from './Pages/HomeScreen/HomeScreen'

function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<HomeScreen/>}/>
          <Route path='/callback' element={<Callback/>} />
          <Route path="/playlist" element={<CreatePlaylist/>}/>
          <Route path="/UserPlaylists" element={<UserPlaylists/>}/>
          <Route path='/loading' element={<Loading/>}/>
        </Routes>
      </Router>
    </>
  )
}

export default App
