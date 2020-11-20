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
    Marker,
    TileLayer,
    Popup,
    Pane,
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
        // Constrains map on page (WIP)
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
                    {/* Creates a rectangle. As of right now it just sits there */}
                    <Pane name="cyan-rectangle" style={{ zIndex: 500 }}>
                        <Rectangle bounds={[[48.5, 1], [48.7, 1.3]]} pathOptions={{ color: 'cyan' }} />
                    </Pane>
                    {this.props.mapData.map((mapSquareData) => {
                        // console.log(mapSquareData.number);
                        const index = mapSquareData.number;
                        const coords = mapSquareData.topLeftCoords;
                        const numberOfPhotos = mapSquareData.photos.length;
                        const position = [coords.lat, coords.lng];
                        const link = '/map_square/' + index;
                        return (
                            <Marker key={index} position={position}>
                                <Popup> Map square {index} <br />
                                    <a href={link}>{numberOfPhotos} photos to show</a>
                                </Popup>
                            </Marker>
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
