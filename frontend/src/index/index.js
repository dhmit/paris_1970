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
} from 'react-leaflet';

import Navbar from '../about/navbar';
import { Footer } from '../UILibrary/components';

class Map extends React.Component {
    state = {
        lat: 48.858859,
        lng: 2.3470599,
        zoom: 13,
    }

    render() {
        const style = {
            marginTop: '60px',
            marginBottom: '60px',
        };
        return (
            <div style={style}>
            <LeafletMap
                center={[this.state.lat, this.state.lng]}
                zoom={this.state.zoom}
                style={{ width: '100%', height: '900px' }}

                // Sets Map Boundaries
                // maxBoundsViscosity={1.0}
                // maxBounds={[[48.082142, 0.854779], [49.464403, 3.761125]]}
                // maxZoom={20}
            >
                <TileLayer
                    // Sets Map Boundaries
                    // bounds={[[48.082142, 0.854779], [49.464403, 3.761125]]}
                    // maxZoom={20}
                    // maxBoundsViscosity={1.0}
                    attribution='&copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {this.props.mapData.map((mapSquareData, index) => {
                    const coords = mapSquareData.topLeftCoords;
                    const position = [coords.lat, coords.lng];
                    return (
                        <Marker key={index} position={position}/>
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

            // @TODO: THIS IS ALL FAKE FOR PROTOTYPING
            // REMOVE ME BEFORE PR!
            // REMOVE ME BEFORE PR!
            // REMOVE ME BEFORE PR!
            // REMOVE ME BEFORE PR!
            // Add fake coordinates to all of the map squares
            const mapSquareCoords = {
                7: [48.889563, 2.298052],
                120: [48.894622, 2.385649],
            };
            let lat = 48.889563;
            let lng = 2.298052;
            // for (const mapSquare of mapData) {
            //     console.log(mapSquare);
            //     if (mapSquare.number === 7 || mapSquare.number === 120) {
            //         console.log(mapSquare, 'HIIII');
            //         lat = mapSquareCoords.mapSquare.number[0];
            //         lng = mapSquareCoords.mapSquare.number[1];
            //         mapSquare.topLeftCoords = {
            //             lat,
            //             lng
            //     };
            //     }
            // }

            for (const mapSquare of mapData) {
                mapSquare.topLeftCoords = { lat, lng };
                lat += 0.005;
                lng += 0.005;
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
