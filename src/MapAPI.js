import React from 'react'
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';


const containerStyle = {
  width: '800px',
  height: '800px'
};

let center = {
  lat: -3.745,
  lng: -38.523
};

function Map() {
  const [map, setMap] = React.useState(null)
  const onLoad = React.useCallback(function callback(map) {
    const bounds = new window.google.maps.LatLngBounds();
    map.fitBounds(bounds);
    setMap(map)
  }, [])

  const onUnmount = React.useCallback(function callback(map) {
    setMap(null)
  }, [])

  return (
    <LoadScript
      googleMapsApiKey="AIzaSyCaqLHmoHvFy_t4H3EZiuvHOmcm2nbt0bI"
    >
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={{lat: 0, lng: 20}}
        zoom={10}
        onLoad={onLoad}
        onUnmount={onUnmount}
      >
        {<Marker position={{ lat: -34.397, lng: 150.644 }} />}
        <></>
      </GoogleMap>
    </LoadScript>
  )
}


function Pin(lat, lon, local){
    return (
        {
            lat: lat,
            lon: lon,
            color: local ? 'red' : 'blue',
            descriptor: "",
            addDescription: (str) => {
                this.descriptor = str;
            }
        }
    )
}

function PinStack(pins){
    return (
        <div>
            pins.map(function(pin) {
                return <Marker position={{lat: pin.lat, lng: pin.lon}} />;
            });
        </div>
    )
}

export default React.memo(Map)