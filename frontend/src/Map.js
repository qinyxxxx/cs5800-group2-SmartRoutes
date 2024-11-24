import React, { useState, useEffect } from 'react';
import './Map.css'; // Import the CSS file

function Map() {
  const [map, setMap] = useState(null);
  const [locations, setLocations] = useState([]);
  const [maxLocations] = useState(5);
  const [route, setRoute] = useState(null); 
  const [totalDistance, setTotalDistance] = useState(null); 

  useEffect(() => {
    window.initMap = () => {
      const mapInstance = new window.google.maps.Map(document.getElementById('map'), {
        center: { lat: 37.7749, lng: -122.4194 },
        zoom: 10,
        mapTypeId: 'roadmap',
      });

      setMap(mapInstance);

      mapInstance.addListener('click', (event) => {
        if (locations.length < maxLocations) {
          const lat = event.latLng.lat();
          const lng = event.latLng.lng();
          const clickedLocation = { lat, lng, id: Date.now() };

          setLocations((prevLocations) => [clickedLocation, ...prevLocations]);

          new window.google.maps.Marker({
            position: clickedLocation,
            map: mapInstance,
            title: `Location ${locations.length + 1}`,
          });
        } else {
          alert(`You can only select ${maxLocations} locations.`);
        }
      });
    };

    if (!window.google) {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.REACT_APP_GOOGLE_MAPS_API_KEY}&libraries=places&callback=initMap`;
      script.async = true;
      document.head.appendChild(script);
    } else {
      window.initMap();
    }
  }, [locations]);

  const handleRemoveLocation = (id) => {
    setLocations(locations.filter(location => location.id !== id));
  };

  const calculateShortestRoute = async () => {
    if (locations.length < 2) {
      alert('Please select at least two locations.');
      return;
    }

    const locationsData = locations.map(location => ({ lat: location.lat, lng: location.lng }));

    try {
      const response = await fetch('http://127.0.0.1:5000/calculate_route', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ locations: locationsData }),
      });
      const data = await response.json();

      setRoute(data.route);
      setTotalDistance(data.totalDistance);

      drawRouteOnMap(data.route);
    } catch (error) {
      console.error('Error calculating route:', error);
    }
  };

  const drawRouteOnMap = (route) => {
    const path = route.map(location => new window.google.maps.LatLng(location.lat, location.lng));

    const routePath = new window.google.maps.Polyline({
      path,
      geodesic: true,
      strokeColor: '#FF0000',
      strokeOpacity: 1.0,
      strokeWeight: 2,
    });
    routePath.setMap(map);
  };

  return (
    <div className="map-container">
      <h2>Select Locations on the Map</h2>
      <p>Click on the map to select locations. You can select up to {maxLocations} locations.</p>
      <div id="map" />
      
      <h3>Locations You Picked:</h3>
      <ul className="locations-list">
        {locations.map((location) => (
          <li key={location.id}>
            {`Location ${locations.indexOf(location) + 1}: Lat: ${location.lat}, Lng: ${location.lng}`}
            <button onClick={() => handleRemoveLocation(location.id)}>Remove</button>
          </li>
        ))}
      </ul>

      <button onClick={calculateShortestRoute}>Calculate</button>

      {route && (
        <div className="route-info">
          <h3>Route:</h3>
          <ul>
            {route.map((location, index) => (
              <li key={index}>{`Location ${index + 1}: Lat: ${location.lat}, Lng: ${location.lng}`}</li>
            ))}
          </ul>
          <p>Total Distance: {totalDistance} km</p>
        </div>
      )}
    </div>
  );
}

export default Map;
