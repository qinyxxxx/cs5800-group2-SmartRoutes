import React, { useState, useEffect, useRef } from "react";
import loadGoogleMaps from "../loadGoogleMaps";
import "../Map.css";

function Map() {
  const [locations, setLocations] = useState(["", ""]);
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);
  const [geocoder, setGeocoder] = useState(null);
  const directionsService = useRef(null);
  const directionsRenderer = useRef(null);
  const [routeOrder, setRouteOrder] = useState([]);

  useEffect(() => {
    const apiKey = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;
    loadGoogleMaps(apiKey)
      .then(() => {
        initMap();
      })
      .catch((err) => {
        console.error("Failed to load Google Maps API:", err);
      });
  }, []);

  const initMap = () => {
    const mapInstance = new window.google.maps.Map(mapRef.current, {
      center: { lat: 37.3375381, lng: -121.8897467 },
      zoom: 15,
      mapTypeId: "roadmap",
    });
    setMap(mapInstance);
    directionsService.current = new window.google.maps.DirectionsService();
    directionsRenderer.current = new window.google.maps.DirectionsRenderer();
    directionsRenderer.current.setMap(mapInstance);
    setGeocoder(new window.google.maps.Geocoder());
  };

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
    locations.forEach((location) => {
      if (location.trim() !== "" && geocoder) {
        geocoder.geocode({ address: location }, (results, status) => {
          if (status === "OK") {
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
    const waypoints = locations.slice(1, -1).map((location) => ({ location, stopover: true }));
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
          if (status === "OK") {
            directionsRenderer.current.setDirections(response);

            const legs = response.routes[0].legs;
            const order = legs.map((leg, index) => ({
              step: index + 1,
              start: leg.start_address,
              end: leg.end_address,
            }));
            setRouteOrder(order);
          } else {
            window.alert("Directions request failed due to " + status);
          }
        }
      );
    } else {
      console.error("DirectionsService or DirectionsRenderer is not initialized.");
    }
  };

  const fetchTSPRoute = async () => {
    if (locations.length < 2) {
      alert("Please enter at least two locations.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/greedy", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ locations }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch TSP route from API");
      }

      const data = await response.json();
      if (data.success) {
        const { orderedLocations } = data;
        calculateTSPRoutes(orderedLocations);
      } else {
        alert("TSP calculation failed: " + data.message);
      }
    } catch (error) {
      console.error("Error fetching TSP route:", error);
      alert("Error fetching TSP route. Please try again.");
    }
  };

  const calculateTSPRoutes = (orderedLocations) => {
    if (orderedLocations.length < 2) {
      alert("Please enter at least two locations.");
      return;
    }

    const waypoints = orderedLocations.slice(1, -1).map(location => ({ location, stopover: true }));
    const origin = orderedLocations[0];
    const destination = orderedLocations[orderedLocations.length - 1];

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
            const legs = response.routes[0].legs;
            const order = legs.map((leg, index) => ({
              step: index + 1,
              start: leg.start_address,
              end: leg.end_address,
            }));
            setRouteOrder(order); // 更新路线顺序
          } else {
            window.alert('Directions request failed due to ' + status);
          }
        }
      );
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
                  <button onClick={() => removeInput(index)} className="remove-btn">
                    -
                  </button>
              )}
              {index === locations.length - 1 && (
                  <button onClick={addInput} className="add-btn">
                    +
                  </button>
              )}
            </div>
        ))}
        {/*<button onClick={submitLocations}>Mark Locations on Map</button>*/}
        <br/>
        {/*<button onClick={calculateRoutes}>Calculate Routes</button>*/}
        <button onClick={fetchTSPRoute}>Greedy TSP</button>
        <div id="map" ref={mapRef} style={{height: "500px", width: "100%"}}></div>

        {routeOrder.length > 0 && (
            <div className="route-order">
              <h3>Route Order:</h3>
              <ol>
                {routeOrder.map(({step, start, end}) => (
                    <li key={step}>
                      <strong>Step {step}:</strong> {start} → {end}
                    </li>
                ))}
              </ol>
            </div>
        )}
      </div>
  );
}

export default Map;