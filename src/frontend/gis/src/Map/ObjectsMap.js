import React from 'react';
import {MapContainer, TileLayer} from 'react-leaflet';
import ObjectMarkersGroup from "./ObjectMarkersGroup";

function ObjectsMap() {
    return (
        <MapContainer style={{width: "100%", height: "100vh"}}
                      center={[37.875499649999995, -122.23906851395179]}
                      zoom={13}
                      scrollWheelZoom={false}
        >
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <ObjectMarkersGroup/>
        </MapContainer>
    );
}

export default ObjectsMap;