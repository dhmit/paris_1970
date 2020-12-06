/*
  The landing page for the prototyping environment.
 *
 * PLEASE NOTE: this is not going to go into the EdX course.
 * It's just for our convenience while developing,
 * so DO NOT spend too much time making this nice!
 */

import React from 'react';
import * as PropTypes from 'prop-types';
import {
    Map as LeafletMap,
    TileLayer,
    Popup,
    Rectangle,
} from 'react-leaflet';

import Navbar from '../about/navbar';
import { Footer } from '../UILibrary/components';

class Map extends React.Component {
    state = {
        lat: 48.858859,
        lng: 2.3470599,
        zoom: 13,
        bounds: [[48.082142, 0.854779], [49.464403, 3.761125]],
        minZoom: 10,
    }

    render() {
        return (
            <div id="mapContainer">
                <LeafletMap
                    // Initial state of Map
                    center={[this.state.lat, this.state.lng]}
                    zoom={this.state.zoom}
                    style={{ width: '100%', height: '75vh' }}
                    // Sets Map Boundaries - Keeps user from leaving Paris
                    maxBoundsViscosity={1.0}
                    maxBounds={this.state.bounds}
                    minZoom={this.state.minZoom}
                >
                    <TileLayer
                        // Sets Map Boundaries - Keeps user from leaving Paris
                        maxBoundsViscosity={1.0}
                        bounds={this.state.bounds}
                        minZoom={this.state.minZoom}
                        // Retrieves Map image
                        attribution='&copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />

                    {this.props.mapData.map((mapSquareData) => {
                        const index = mapSquareData.number;
                        const coords = mapSquareData.topLeftCoords;
                        const numberOfPhotos = mapSquareData.photos.length;

                        // Difference of 250m in coords
                        const lngdiff = 0.01361302273;
                        const latdiff = 0.011179;

                        const msbounds = [[(coords.lat), (coords.lng)],
                                    [(coords.lat - latdiff), (coords.lng - lngdiff)]];
                        const link = '/map_square/' + index;
                        return (
                            <Rectangle key={index} bounds={msbounds} pathOptions={{ color: 'cyan' }}>
                                <Popup>
                                    Map Square {index} <br />
                                    <a href={link}>{numberOfPhotos} photos to show</a>
                                </Popup>
                            </Rectangle>
                        );
                    })}
                </LeafletMap>
            </div>
        );
    }
}
Map.propTypes = {
    mapData: PropTypes.array,
};


export class IndexView extends React.Component {
    state = {
        incidents: [],
    }

    async componentDidMount() {
        try {
            const mapResponse = await fetch('/api/all_map_squares/');
            const mapData = await mapResponse.json();

            for (const mapSquare of mapData) {
                // This code right here might cause problems if said user hasn't run syncdb
                const roughCoords = mapSquare.rough_coords;

                // If the map square has coordinates in the spreadsheet, it pulls those coordinates
                // and makes those the coordinates of the marker (NOTE: This is entirely reliant
                // on things being in the form of "lat, lng")

                // If the map square does not have the coordinates in the spread sheet, it sets
                // them to (0, 0)
                if (roughCoords) {
                    const roughCoordsList = roughCoords.split(', ');
                    const lat = parseFloat(roughCoordsList[0]);
                    const lng = parseFloat(roughCoordsList[1]);
                    // console.log(lat);
                    // console.log(lng);
                    mapSquare.topLeftCoords = { lat, lng };
                } else {
                    const lat = 0.0;
                    const lng = 0.0;
                    mapSquare.topLeftCoords = { lat, lng };
                }
            }

            this.setState({
                mapData,
                loading: false,
            });
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        if (!this.state.mapData) {
            return (<>
                Loading...
            </>);
        }

        return (<React.Fragment>
            <Navbar />
            <Map mapData={this.state.mapData} />
            <Footer />
        </React.Fragment>);
    }
}
export default IndexView;
