import React, {useState} from "react";

import * as PropTypes from "prop-types";
import {
    MapContainer,
    TileLayer,
    Popup,
    Rectangle,
    ZoomControl
} from "react-leaflet";

import {
    Modal,
    Button
} from "react-bootstrap";

import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import LoadingPage from "./LoadingPage";

import Legend from "../components/Legend.js";

class Map extends React.Component {
    state = {
        lat: 48.858859,
        lng: 2.3470599,
        zoom: 13,
        bounds: [[48.8030, 2.1330], [48.9608, 2.6193]],
        minZoom: 12
    };

    render() {
        console.log("MAP STATE", this.state);
        // Sorts the map squares by number of photos (ascending order)
        const sortedMapData = Object.values(this.props.mapData)
        .sort((a, b) => a.num_photos - b.num_photos);
        // Gets the max number of photos in a single square out of all squares to form buckets later
        const maxNumOfPhotos = sortedMapData && sortedMapData.length
            ? sortedMapData[sortedMapData.length - 1].num_photos
            : 0;
        // Creating 5 buckets based on lowest to highest number of photos per square
        const twentyPctMax = Math.round(0.2 * maxNumOfPhotos);
        const fortyPctMax = Math.round(0.4 * maxNumOfPhotos);
        const sixtyPctMax = Math.round(0.6 * maxNumOfPhotos);
        const eightyPctMax = Math.round(0.8 * maxNumOfPhotos);
        const buckets = [0, twentyPctMax, twentyPctMax + 1,
            fortyPctMax, fortyPctMax + 1,
            sixtyPctMax, sixtyPctMax + 1,
            eightyPctMax, eightyPctMax + 1, maxNumOfPhotos];
        console.log("index.js technically here??");
        return (
            <div id="map-container">
                <Instructions/>
                <MapContainer
                    // Initial state of Map
                    center={[this.state.lat, this.state.lng]}
                    zoom={this.state.zoom}
                    style={{
                        width: "100%",
                        height: "500px"
                    }}
                    // Sets Map Boundaries - Keeps user from leaving Paris
                    maxBoundsViscosity={1.0}
                    maxBounds={this.state.bounds}
                    minZoom={this.state.minZoom}
                    zoomControl={false}>
                    <ZoomControl position="bottomleft"/>
                    <Legend buckets={buckets}/>
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

                    {
                        sortedMapData.map((mapSquareData) => {
                            const index = mapSquareData.number;
                            const coords = mapSquareData.topLeftCoords;
                            const numberOfPhotos = mapSquareData.num_photos;
                            // Width and height of map squares
                            const lngDiff = 0.00340325568;
                            const latDiff = 0.0022358;

                            const mapSquareBounds = [
                                [coords.lat, coords.lng],
                                [coords.lat - latDiff, coords.lng - lngDiff]
                            ];
                            const link = "/map_square/" + index;
                            let mapSquareBucket = "";
                            // set of conditionals to to calculate photo density for heat map
                            if (numberOfPhotos > 0 && numberOfPhotos <= twentyPctMax) {
                                mapSquareBucket = "map-square box-one";
                            } else if (numberOfPhotos <= fortyPctMax) {
                                mapSquareBucket = "map-square box-two";
                            } else if (numberOfPhotos <= sixtyPctMax) {
                                mapSquareBucket = "map-square box-three";
                            } else if (numberOfPhotos <= eightyPctMax) {
                                mapSquareBucket = "map-square box-four";
                            } else if (numberOfPhotos <= maxNumOfPhotos) {
                                mapSquareBucket = "map-square box-five";
                            }
                            // Greys out squares without photos in them
                            if (numberOfPhotos === 0) {
                                return (
                                    <Rectangle className="map-grid"
                                               key={index}
                                               bounds={mapSquareBounds}>
                                        <Popup>
                                            Map Square {index} <br/>
                                            <a href={link}>{numberOfPhotos} photos to show</a>
                                        </Popup>
                                    </Rectangle>
                                );
                            }

                            return (
                                <Rectangle className={mapSquareBucket}
                                           key={index}
                                           bounds={mapSquareBounds}>
                                    <Popup className={"map-popup"}>
                                        Map Square {index} <br/>
                                        <a href={link}>{numberOfPhotos} photos to show</a>
                                    </Popup>
                                </Rectangle>
                            );
                        })
                    }
                </MapContainer>
            </div>
        );
    }
}

Map.propTypes = {
    mapData: PropTypes.array
};


function Instructions() {
    const [show, setShow] = useState(true);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    return (
        <>
            <Button id="instructionButton" variant="primary" onClick={handleShow}>
                Instructions
            </Button>
            <Modal
                show={show}
                onHide={handleClose}
                backdrop="static"
                keyboard={false}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered>
                <Modal.Header closeButton>
                    <Modal.Title>Welcome</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Welcome to the map view of Paris in 1970! The images in this archive are from
                    a photography competition in 1970's Paris hosted to capture Paris before
                    rapid industrial change altered the city permanently.
                </Modal.Body>
                <Modal.Body>
                    To explore images from specific areas of Paris, click on a highlighted square.
                    You will see the map square number and how many images are available.
                    Click on the link to see the images from that area!
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="primary" onClick={handleClose}>
                        Got it!
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
}


export class HomePage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mapData: null
        };
    }

    async componentDidMount() {
        try {
            const mapResponse = await fetch("/api/all_map_squares/");
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
                    const roughCoordsList = roughCoords.split(", ");
                    const lat = parseFloat(roughCoordsList[0]);
                    const lng = parseFloat(roughCoordsList[1]);
                    mapSquare.topLeftCoords = {
                        lat,
                        lng
                    };
                } else {
                    const lat = 0.0;
                    const lng = 0.0;
                    mapSquare.topLeftCoords = {
                        lat,
                        lng
                    };
                }
            }

            this.setState({
                mapData,
                loading: false
            });
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        if (!this.state.mapData) {
            return (<LoadingPage/>);
        }

        return (<>
            <Navbar/>
            <Map mapData={this.state.mapData}/>
            <Footer/>
        </>);
    }
}

export default HomePage;
