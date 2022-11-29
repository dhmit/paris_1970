import React from "react";
import ParisMap, {MAPSQUARE_HEIGHT, MAPSQUARE_WIDTH} from "../components/ParisMap";
import * as PropTypes from "prop-types";
import PhotoViewer from "../components/PhotoViewer";
import LoadingPage from "./LoadingPage";
import {GeoJSON, Popup, Rectangle} from "react-leaflet";

function densityOverlay(mapSquareData) {
    const sortedMapData = Object.values(mapSquareData)
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
    return (<>
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
}

function arrondissementsOverlay(data) {
    return data !== null ? data.map(tract => {
        return (
            <GeoJSON
                style={{
                    fillColor: "none",
                    color: "#20CCD7"
                }}
                key={tract.properties["GISJOIN"]}
                data={tract}
            />
        );
    }) : <></>;
}

class TagView extends PhotoViewer {
    constructor(props) {
        super(props);

        this.state = {
            mapData: null,
            geojsonData: null,
            filledMapSquares: null,
            filledMapSquaresData: null,
            isLgViewportUp: null,
            mapSquare: null,
            photos: JSON.parse(this.props.tagPhotos),
            photographers: []
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
                let lat = 0;
                let lng = 0;
                if (roughCoords) {
                    const roughCoordsList = roughCoords.split(", ");
                    lat = parseFloat(roughCoordsList[0]);
                    lng = parseFloat(roughCoordsList[1]);
                }
                mapSquare.topLeftCoords = {
                    lat,
                    lng
                };
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

            //Makes a set of all map squares with num_photos equal to the number of pictures for the current tag
            const filledMapSquares = new Set();
            const filledMapSquaresData = {};
            for (const photo of this.state.photos) {
                const photoMapSquare = this.state.mapData[photo["map_square_number"]-1];
                const photoMapSquareNumber = photo["map_square_number"];
                filledMapSquares.add(photoMapSquare["id"]);
                if (!filledMapSquaresData[photoMapSquareNumber]){
                    filledMapSquaresData[photoMapSquareNumber] = photoMapSquare;
                    filledMapSquaresData[photoMapSquareNumber].num_photos = 0;
                }
                filledMapSquaresData[photoMapSquareNumber].num_photos += 1;
            }
            for (const mapSquare of this.state.mapData) {
                if (!filledMapSquaresData[mapSquare["id"]]) {
                    filledMapSquaresData[mapSquare["id"]] = mapSquare;
                    filledMapSquaresData[mapSquare["id"]].num_photos = 0;
                }
            }
            this.setState({
                filledMapSquares: filledMapSquares,
                filledMapSquaresData: filledMapSquaresData,
                geojsonData: geojsonData["features"],
                loading: false
            });
        } catch (e) {
            console.log(e);
        }

    }


    render() {

        if (this.props.tagPhotos.length === 0) {
            return (<>
                Tag {this.props.tagName} is not in the database.
            </>);
        }
        const tag = this.props.tagName;
        const photos = JSON.parse(this.props.tagPhotos);

        if (!this.state.mapData || !this.state.filledMapSquares || !this.state.filledMapSquaresData) {
            return (<LoadingPage/>);
        }
        return (<>
            <div className="row">
                <div className="tag-info col-12 col-lg-5">
                    <p className="tag-header">Photographs tagged</p>
                    <p className="tag-title">{tag}</p>
                    <ul className="p-0">{this.getPhotoGrid(photos, {"photoSize": [120, 120]})}</ul>
                </div>
                <div className="tag-map col-12 col-lg-7">
                    <ParisMap
                        className="tags-map"
                        zoom={14}
                        layers={{
                            "Arrondissement": arrondissementsOverlay(this.state.geojsonData),
                            "Photos available": densityOverlay(this.state.filledMapSquaresData)
                        }}
                        visibleLayers={["Photos available", "Arrondissement"]} 
                        layerSelectVisible={true}
                    />
                </div>
            </div>
        </>);
    }
}

TagView.propTypes = {
    tagName: PropTypes.string,
    tagPhotos: PropTypes.string
};

export default TagView;
