import React from "react";

import * as PropTypes from "prop-types";
import {
    MapContainer,
    TileLayer,
    ZoomControl,
    GeoJSON
} from "react-leaflet";

export const MAPSQUARE_WIDTH = 0.00340325568;
export const MAPSQUARE_HEIGHT = 0.0022358;


export class ParisMap extends React.Component {
    constructor(props) {
        super(props);

        let visibleLayers = Object.keys(this.props.layers);
        console.log(visibleLayers);
        if (this.props.singleLayer) {
            visibleLayers = this.props.layers[Object.keys(this.props.layers)[0]];
        } else if (this.props.visibleLayers) {
            visibleLayers = this.props.visibleLayers;
        }

        this.state = {
            visibleLayers,
            bounds: [[48.8030, 2.1330], [48.9608, 2.6193]],
            minZoom: 12
        };
    }

    onLayerChange(event) {
        const clickedLayer = event.target.value;
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
        console.log(newVisibleLayers);
    }

    render() {
        console.log("MAP STATE", this.state);
        // Sorts the map squares by number of photos (ascending order)

        console.log("index.js technically here??");
        return (
            <div className={this.props.className} id="map-container">
                <MapContainer
                    // Initial state of Map
                    center={[
                        this.props.lat ? this.props.lat : 48.858859,
                        this.props.lng ? this.props.lng : 2.3470599
                    ]}
                    zoom={this.props.zoom}
                    style={{
                        width: "100%",
                        height: "100%"
                    }}
                    // Sets Map Boundaries - Keeps user from leaving Paris
                    maxBoundsViscosity={1.0}
                    maxBounds={this.state.bounds}
                    minZoom={this.state.minZoom}
                    zoomControl={false}
                >
                    <ZoomControl position="bottomleft"/>
                    <TileLayer
                        // Sets Map Boundaries - Keeps user from leaving Paris
                        maxBoundsViscosity={1.0}
                        bounds={this.state.bounds}
                        minZoom={this.state.minZoom}
                        // Retrieves Map image

                        // HOT option
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>'
                        url="https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"
                    />

                    {Object.keys(this.props.layers).map((layerName) => {
                        return this.state.visibleLayers.includes(layerName)
                            ? this.props.layers[layerName]
                            : <></>;
                    })}
                    {this.props.layerSelectVisible === true ? <div className="card layer-select">
                        <div className="card-body">
                            {Object.keys(this.props.layers).map((layerName, idx) => (
                                <div key={idx}>
                                    <input
                                        className="form-check-input"
                                        type="checkbox"
                                        value={layerName}
                                        checked={this.state.visibleLayers.includes(layerName)}
                                        onChange={(e) => this.onLayerChange(e)}
                                    /> {layerName}
                                </div>
                            ))}
                        </div>
                    </div> : <></>}
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
    layers: PropTypes.object,
    singleLayer: PropTypes.bool,
    layerSelectVisible: PropTypes.bool,
    visibleLayers: PropTypes.array
};

export default ParisMap;
