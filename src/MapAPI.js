import React from 'react'
import { GoogleMap, LoadScript } from '@react-google-maps/api';


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
        center={center}
        zoom={10}
        onLoad={onLoad}
        onUnmount={onUnmount}
      >
        { /* Child components, such as markers, info windows, etc. */ }
        <></>
      </GoogleMap>
    </LoadScript>
  )
}

function Pin(){
    return (
        {
            lat: null,
            lon: null,
            color: 'red'
        }
    )
} 

export default React.memo(Map)