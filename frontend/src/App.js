import React, { useState } from 'react';
import './App.css';
import Map from './Map';

function App() {
  const [coordinates] = useState({ latitude: 37.3382, longitude: -121.8863 });

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to My Simple React Website</h1>
        <p>This is a basic React app created using Create React App.</p>
      </header>

      <Map latitude={coordinates.latitude} longitude={coordinates.longitude} />

    </div>
  );
}

export default App;
