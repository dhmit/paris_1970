import React from "react";

import * as PropTypes from "prop-types";
import {
    MapContainer,
    TileLayer,
    ZoomControl
} from "react-leaflet";
import Legend from "./Legend";

// Measurements in Longitude and Latitude distance respectively.
// Used for creating a grid of all the map squares along with each map squares' approximate
// coordinates.
export const MAPSQUARE_WIDTH = 0.00340325568;
export const MAPSQUARE_HEIGHT = 0.0022358;


export class ParisMap extends React.Component {
    constructor(props) {
        super(props);

        let visibleLayers = Object.keys(this.props.layers);
        if (this.props.singleLayer) {
            visibleLayers = this.props.layers[Object.keys(this.props.layers)[0]];
        } else if (this.props.visibleLayers) {
            visibleLayers = this.props.visibleLayers;
        }

        this.state = {
            visibleLayers,
            layers: ["Arrondissement", "Photo Density"],
            bounds: [[48.8030, 2.1330], [48.9608, 2.6193]],
            minZoom: 12,
            zoom: this.props.zoom
        };
        this.toggleLayer = this.toggleLayer.bind(this);
    }

    toggleLayer(event) {
        const clickedLayer = event.target.dataset.value;
        let newVisibleLayers = this.state.visibleLayers;
        if (this.props.singleLayer) {
            newVisibleLayers = [];
        }
        if (newVisibleLayers.includes(clickedLayer)) {
            newVisibleLayers.splice(newVisibleLayers.indexOf(clickedLayer), 1);
        } else {
            newVisibleLayers.push(clickedLayer);
        }
        this.setState({visibleLayers: newVisibleLayers});
    }

    render() {
        // Sorts the map squares by number of photos (ascending order)
        return (
            <div className={this.props.className} id="map-container">
                <Legend layers={this.state.layers}
                        toggleLayer={this.toggleLayer}
                        visibleLayers={this.state.visibleLayers}/>
                <MapContainer key={this.props.scrollWheelZoom}
                    // Initial state of Map
                              center={[
                                  this.props.lat ? this.props.lat : 48.858859,
                                  this.props.lng ? this.props.lng : 2.3470599
                              ]}
                              zoom={this.state.zoom}

                              scrollWheelZoom={this.props.scrollWheelZoom}
                              style={{
                                  width: "100%",
                                  height: "100%"
                              }}
                    // Sets Map Boundaries - Keeps user from leaving Paris
                              maxBoundsViscosity={1.0}
                              maxBounds={this.state.bounds}
                              minZoom={this.state.minZoom}
                              zoomControl={false}>
                    <ZoomControl position="bottomleft"/>
                    <TileLayer
                        // Sets Map Boundaries - Keeps user from leaving Paris
                        maxBoundsViscosity={1.0}
                        bounds={this.state.bounds}
                        minZoom={this.state.minZoom}
                        // Retrieves Map image

                        // HOT option
                        url="http://stamen-tiles-a.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}.png"
                    />

                    {Object.keys(this.props.layers)
                    .map((layerName) => {
                        return this.state.visibleLayers.includes(layerName)
                            ? this.props.layers[layerName]
                            : <></>;
                    })}
                </MapContainer>
            </div>
        );
    }
}

ParisMap.propTypes = {
    className: PropTypes.string,
    lat: PropTypes.number,
    lng: PropTypes.number,
    zoom: PropTypes.number,
    scrollWheelZoom: PropTypes.bool,
    layers: PropTypes.object,
    singleLayer: PropTypes.bool,
    layerSelectVisible: PropTypes.bool,
    visibleLayers: PropTypes.array
};

export default ParisMap;
