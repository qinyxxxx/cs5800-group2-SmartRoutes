import React, { useState } from 'react';
import './App.css';
import Map from './components/Map';

function App() {
  const [coordinates] = useState({ latitude: 37.3382, longitude: -121.8863 });

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to Smart Routes</h1>
        <p>Designed by: Yuxin Qin, Yanlu He, Xiangying Sun</p>
      </header>

      <Map latitude={coordinates.latitude} longitude={coordinates.longitude} />

      <footer className="App-footer">
        <p>© Smart Routes Team</p>
      </footer>

    </div>
  );
}

export default App;
