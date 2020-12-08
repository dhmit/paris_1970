/*
  The landing page for the prototyping environment.
 *
 * PLEASE NOTE: this is not going to go into the EdX course.
 * It's just for our convenience while developing,
 * so DO NOT spend too much time making this nice!
 */
/* '#02bfe7' */
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
        bounds: [[48.8030, 2.1330], [48.9608, 2.6193]],
        minZoom: 12,
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
                    {
                        // TODO: sort this.props.mapData so empty map squares drawn first, map
                        // squares with photos drawn last
                    }
                    {this.props.mapData.map((mapSquareData) => {
                        const index = mapSquareData.number;
                        const coords = mapSquareData.topLeftCoords;
                        const numberOfPhotos = mapSquareData.photos.length;

                        // Width and height of map squares
                        const lngdiff = 0.00340325568;
                        const latdiff = 0.0022358;

                        const msbounds = [[(coords.lat), (coords.lng)],
                            [(coords.lat - latdiff), (coords.lng - lngdiff)]];
                        const link = '/map_square/' + index;

                        // Greys out squares without photos in them
                        if (numberOfPhotos === 0) {
                            return (
                                <Rectangle key={index} bounds={msbounds} color={'#b3b3b3'} weight={2}>
                                    <Popup>
                                        Map Square {index} <br />
                                        <a href={link}>{numberOfPhotos} photos to show</a>
                                    </Popup>
                                </Rectangle>
                            );
                        }
                        return (
                            <Rectangle key={index} bounds={msbounds} color={'#b51a00'} weight={4}>
                                <Popup>
                                    Map Square {index} <br/>
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
                const roughCoords = mapSquare.coordinates;

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
