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
        // Sorts the map squares by number of photos (ascending order)
        const sortedMapData = Object.values(this.props.mapData)
            .sort((a, b) => a.photos.length - b.photos.length);

        return (
            <div id="map-container">
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

                        // HOT option
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>'
                        url="https://tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"



                    />

                    {
                        sortedMapData.map((mapSquareData) => {
                            const index = mapSquareData.number;
                            const coords = mapSquareData.topLeftCoords;
                            const numberOfPhotos = mapSquareData.photos.length;

                            // Width and height of map squares
                            const lngDiff = 0.00340325568;
                            const latDiff = 0.0022358;

                            const mapSquareBounds = [
                                [coords.lat, coords.lng],
                                [coords.lat - latDiff, coords.lng - lngDiff],
                            ];
                            const link = '/map_square/' + index;

                            // Greys out squares without photos in them
                            if (numberOfPhotos === 0) {
                                return (
                                    <Rectangle
                                        key={index}
                                        bounds={mapSquareBounds}
                                        color={'#d06c5a'} weight={2}
                                        opacity={0.45}
                                        fillOpacity={0}

                                    >
                                        <Popup>
                                            Map Square {index} <br />
                                            <a href={link}>{numberOfPhotos} photos to show</a>
                                        </Popup>
                                    </Rectangle>
                                );
                            }
                            return (
                                <Rectangle
                                    key={index}
                                    bounds={mapSquareBounds}
                                    color={'#008fd4'} weight={1}

                                >
                                    <Popup>
                                        Map Square {index} <br/>
                                        <a href={link}>{numberOfPhotos} photos to show</a>
                                    </Popup>
                                </Rectangle>
                            );
                        })
                    }
                </LeafletMap>
            </div>
        );
    }
}
Map.propTypes = {
    mapData: PropTypes.array,
};


export class IndexView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mapData: null,
        };
    }

    async componentDidMount() {
        try {
            const mapResponse = await fetch('/api/all_map_squares/');
            const mapData = await mapResponse.json();

            for (const mapSquare of mapData) {
                // This code right here might cause problems if said user hasn't run syncdb
                const roughCoords = mapSquare.coordinates;

                // If the map square has coordinates in the spreadsheet,
                // it pulls those coordinates and makes those the coordinates of the marker
                // Coords must be in (lat, lng)

                // If the map square does not have the coordinates it sets them to (0, 0)
                // NOTE(ra): this no longer happens, so we can probably remove this safety check
                if (roughCoords) {
                    const roughCoordsList = roughCoords.split(', ');
                    const lat = parseFloat(roughCoordsList[0]);
                    const lng = parseFloat(roughCoordsList[1]);
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
