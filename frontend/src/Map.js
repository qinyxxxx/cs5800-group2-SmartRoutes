import React, { useState, useEffect, useRef } from 'react';

function Map() {
  const [locations, setLocations] = useState(["", ""]);
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);
  const [geocoder, setGeocoder] = useState(null);
  const directionsService = useRef(null);
  const directionsRenderer = useRef(null);

  useEffect(() => {
    const loadScript = () => {
      if (!document.querySelector('script[src*="maps.googleapis.com"]')) {
        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.REACT_APP_GOOGLE_MAPS_API_KEY}&libraries=places`;
        script.async = true;
        script.defer = true;
        script.onload = () => {
          initMap();
        };
        document.body.appendChild(script);
      } else {
        initMap();
      }
    };

    const initMap = () => {
      const mapInstance = new window.google.maps.Map(mapRef.current, {
        center: { lat: 37.3375381, lng: -121.8897467 },
        zoom: 15,
        mapTypeId: 'roadmap',
      });
      setMap(mapInstance);
      directionsService.current = new window.google.maps.DirectionsService();
      directionsRenderer.current = new window.google.maps.DirectionsRenderer();
      directionsRenderer.current.setMap(mapInstance);
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

  // 标记位置
  const submitLocations = () => {
    locations.forEach((location) => {
      if (location.trim() !== '' && geocoder) {
        geocoder.geocode({ address: location }, (results, status) => {
          if (status === 'OK') {
            const { lat, lng } = results[0].geometry.location;
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


  const calculateRoutes = () => {
    if (locations.length < 2) {
      alert("Please enter at least two locations.");
      return;
    }
    const waypoints = locations.slice(1, -1).map(location => ({ location, stopover: true }));
    const origin = locations[0];
    const destination = locations[locations.length - 1];

    if (directionsService.current && directionsRenderer.current) {
      directionsService.current.route(
        {
          origin,
          destination,
          waypoints,
          travelMode: window.google.maps.TravelMode.DRIVING,
        },
        (response, status) => {
          if (status === 'OK') {
            directionsRenderer.current.setDirections(response); // 渲染路线
          } else {
            window.alert('Directions request failed due to ' + status);
          }
        }
      );
    } else {
      console.error("DirectionsService or DirectionsRenderer is not initialized.");
    }
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
      <button onClick={calculateRoutes}>Calculate Routes</button>
      <div id="map" ref={mapRef} style={{ height: '500px', width: '100%' }}></div>
    </div>
  );
}

export default Map;