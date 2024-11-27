import React, { useState, useEffect, useRef } from 'react';
import './Map.css';

function Map() {
  const [locations, setLocations] = useState(["", ""]); // 默认两个输入框
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);
  const [geocoder, setGeocoder] = useState(null);

  useEffect(() => {
    const loadScript = () => {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.REACT_APP_GOOGLE_MAPS_API_KEY}&libraries=places&callback=initMap`;
      script.async = true;
      script.defer = true;
      document.body.appendChild(script);
    };

    window.initMap = () => {
      const mapInstance = new window.google.maps.Map(mapRef.current, {
        center: { lat: 37.3375381, lng: -121.8897467 },
        zoom: 15,
        mapTypeId: 'roadmap',
      });
      setMap(mapInstance);
      setGeocoder(new window.google.maps.Geocoder());
    };

    loadScript();
  }, []);

  const handleLocationInput = (index, event) => {
    const newLocations = [...locations];
    newLocations[index] = event.target.value;
    setLocations(newLocations);
  };

  const addInput = () => {
    setLocations([...locations, ""]);
  };

  const removeInput = (index) => {
    if (locations.length > 2) {
      const newLocations = locations.filter((_, i) => i !== index);
      setLocations(newLocations);
    }
  };

  const submitLocations = () => {
    console.log("helo")
    locations.forEach((location) => {
      console.log("helo22")
      if (location.trim() !== '') {
        console.log("helo2222")
        geocoder.geocode({ address: location }, (results, status) => {
          if (status === 'OK') {
            const { lat, lng } = results[0].geometry.location;
            console.log("lat", lat())
            console.log("lng", lng())
            new window.google.maps.Marker({
              position: { lat: lat(), lng: lng() },
              map: map,
              title: location,
            });
          } else {
            alert(`Geocoding failed for: ${location} with status: ${status}`);
          }
        });
      }
    });
  };

  return (
    <div className="map-container">
      <h2>Enter Locations</h2>
      {locations.map((location, index) => (
        <div key={index} className="input-group">
          <input
            type="text"
            placeholder="Enter full address"
            value={location}
            onChange={(e) => handleLocationInput(index, e)}
            className="location-input"
          />
          {index > 1 && (
            <button onClick={() => removeInput(index)} className="remove-btn">-</button>
          )}
          {index === locations.length - 1 && (
            <button onClick={addInput} className="add-btn">+</button>
          )}
        </div>
      ))}
      <button onClick={submitLocations}>Mark Locations on Map</button>
      <div id="map" ref={mapRef}></div>
    </div>
  );
}

export default Map;