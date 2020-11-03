import React from 'react';
// import * as PropTypes from 'prop-types';
import {
    Map as LeafletMap,
    TileLayer,
} from 'react-leaflet';

export default class Map extends React.Component {
    state = {
        lat: 48.858859,
        lng: 2.3470599,
        zoom: 13,
    }

    render() {
        return (
            <LeafletMap
                center={[this.state.lat, this.state.lng]}
                zoom={this.state.zoom}
                style={{ width: '100%', height: '900px' }}
            >
                <TileLayer
                    attribution='&copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
            </LeafletMap>
        );
    }
}
