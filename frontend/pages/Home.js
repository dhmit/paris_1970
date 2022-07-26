import React from "react";
import {
    Popup,
    Rectangle,
    GeoJSON
} from "react-leaflet";

import Footer from "../components/Footer";
import ParisMap, {MAPSQUARE_HEIGHT, MAPSQUARE_WIDTH} from "../components/ParisMap";
import LoadingPage from "./LoadingPage";
import Legend from "../components/Legend";

import from "../../backend/scripts"

function densityOverlay(mapData) {
    const sortedMapData = Object.values(mapData)
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
    const layer = (<>
        <Legend buckets={buckets}/>

        {
            sortedMapData.map((mapSquareData) => {
                const index = mapSquareData.number;
                const coords = mapSquareData.topLeftCoords;
                const numberOfPhotos = mapSquareData.num_photos;

                const mapSquareBounds = [
                    [coords.lat, coords.lng],
                    [coords.lat - MAPSQUARE_HEIGHT, coords.lng - MAPSQUARE_WIDTH]
                ];
                const link = "/map_square/" + index;
                let mapSquareBucket = "";
                // set of conditionals to calculate photo density for heat map
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

                return (
                    <Rectangle
                        className={numberOfPhotos === 0 ? "map-grid" : mapSquareBucket}
                        key={index}
                        bounds={mapSquareBounds}>
                        <Popup>
                            Map Square {index} <br/>
                            <a href={link}>{numberOfPhotos} photos to show</a>
                        </Popup>
                    </Rectangle>
                );
            })
        }
    </>);
    return layer;
}


function arrondissementsOverlay(data) {
    return data !== null ? data.map(tract => {
        return (
            <GeoJSON
                key={tract.properties["GISJOIN"]}
                data={tract}
            />
        );
    }) : <></>;
}


export class HomePage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mapData: null,
            geojsonData: null
        };
    }

    async componentDidMount() {
        try {
            /*const mapResponse = await fetch("/api/all_map_squares/");
            const mapData = await mapResponse.json();*/

            const mapData =


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
        try {
            const geojsonResponse = await fetch("/api/arrondissements_geojson/");
            const geojsonData = await geojsonResponse.json();
            this.setState({
                geojsonData: geojsonData["features"],
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
            <ParisMap
                className="home-map"
                zoom={14}
                layers={{
                    "Photo Density": densityOverlay(this.state.mapData),
                    "Arrondissements": arrondissementsOverlay(this.state.geojsonData)
                }}
                visibleLayers={["Photo Density"]}
                layerSelectVisible={true}
            />
            <Footer/>
        </>);
    }
}
