import React from "react";
import * as PropTypes from "prop-types";

import {GeoJSON, Tooltip, Rectangle} from "react-leaflet";
import {Container, Row, Col} from "react-bootstrap";

import {debounce} from "../common";

import Map, {MAPSQUARE_HEIGHT, MAPSQUARE_WIDTH} from "../components/ParisMap";
import LoadingPage from "./LoadingPage";
import MapSquareContent from "../components/map-page/MapSquareContent";
import TitleDecoratorContainer from "../components/TitleDecoratorContainer";

function densityOverlay(mapData, selectMapSquare) {
    const sortedMapData = Object.values(mapData).sort((a, b) => a.num_photos - b.num_photos);

    // Gets the max number of photos in a single square out of all squares to form buckets later
    const maxNumOfPhotos =
        sortedMapData && sortedMapData.length
            ? sortedMapData[sortedMapData.length - 1].num_photos
            : 0;

    const percentMax = (percent) => Math.round(percent/100 * maxNumOfPhotos);

    const renderData = [];
    for (const mapSquareData of sortedMapData) {
        const coords = mapSquareData.topLeftCoords;
        const photoCount = mapSquareData.num_photos;
        const number = mapSquareData.number;

        const bounds = [
            [coords.lat, coords.lng],
            [coords.lat - MAPSQUARE_HEIGHT, coords.lng - MAPSQUARE_WIDTH],
        ];
        let rectangleClass = "";

        // Calculate photo density for heat map
        if (photoCount > 0) {
            if (photoCount <= percentMax(20)) {
                rectangleClass = "map-square box-one";
            } else if (photoCount <= percentMax(40)) {
                rectangleClass = "map-square box-two";
            } else if (photoCount <= percentMax(60)) {
                rectangleClass = "map-square box-three";
            } else if (photoCount <= percentMax(80)) {
                rectangleClass = "map-square box-four";
            } else {
                rectangleClass = "map-square box-five";
            }
        } else {
            rectangleClass = "map-grid"; // empty grid
        }


        renderData.push({
            rectangleClass,
            number,
            photoCount,
            bounds,
        });
    }

    return renderData.map(square => (
            <Rectangle
                className={square.rectangleClass}
                key={square.number}
                bounds={square.bounds}
                eventHandlers={
                    square.photoCount
                        ? { click: () => selectMapSquare(square.number) }
                        : null
                }
            >
                <Tooltip permanent={false}>

                    Map Square {square.number} - {square.photoCount} photos
                </Tooltip>
            </Rectangle>
    ));
}

function arrondissementsOverlay(data) {
    return data !== null ? (
        data.map((tract) => {
            return (
                <GeoJSON
                    style={{
                        fillColor: "none",
                        color: "#20CCD7",
                    }}
                    key={tract.properties["GISJOIN"]}
                    data={tract}
                />
            );
        })
    ) : (
        <></>
    );
}

class MapPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            mapData: null,
            geojsonData: null,
            filledMapSquares: null,
            isLgViewportUp: null,
            mapSquare: null,
            mapLat: 48.858859,
            mapLng: 2.3470599,
            photos: [],
        };
        this.selectMapSquare = this.selectMapSquare.bind(this);
        this.updateViewport = this.updateViewport.bind(this);
        this.returnToMap = this.returnToMap.bind(this);
        this.arrondissementData = JSON.parse(this.props.arrondissement_data)["arrondissements"];
        console.log(this.arrondissementData);
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
                        lng,
                    };
                } else {
                    const lat = 0.0;
                    const lng = 0.0;
                    mapSquare.topLeftCoords = {
                        lat,
                        lng,
                    };
                }
            }

            this.setState({
                mapData,
                loading: false,
            });
        } catch (e) {
            console.log(e);
        }
        try {
            const geojsonResponse = await fetch("/api/arrondissements_geojson/");
            const geojsonData = await geojsonResponse.json();

            //Makes a set of all map squares that actually contain pictures. Eventually shouldn't
            //be needed once full picture database is added.
            const filledMapSquares = new Set();

            for (const mapSquare of this.state.mapData) {
                if (mapSquare["num_photos"] > 0) {
                    filledMapSquares.add(mapSquare["id"]);
                }
            }

            this.setState({
                filledMapSquares: filledMapSquares,
                geojsonData: geojsonData["features"],
                loading: false,
            });
        } catch (e) {
            console.log(e);
        }

        this.updateViewport();

        window.addEventListener(
            "resize",
            debounce(() => this.updateViewport(), 250)
        );
    }

    async selectMapSquare(mapSquare) {
        this.setState({mapSquare: mapSquare, photos: []});
        this.state.mapData.map((ms) => {
            if (ms.id === mapSquare) {
                return this.setState({
                    mapLat: ms.topLeftCoords.lat,
                    mapLng: ms.topLeftCoords.lng,
                });
            }
        });
        const mapSquareDetails = await fetch("/api/map_square/" + mapSquare);
        const mapSquareDetailsJSON = await mapSquareDetails.json();
        this.setState({
            photos: mapSquareDetailsJSON.photos,
        });
    }

    updateViewport() {
        this.setState({isLgViewportUp: window.innerWidth > 992});
    }

    returnToMap() {
        this.setState({mapSquare: null});
    }

    render() {
        if (
            !this.state.mapData ||
            !this.state.filledMapSquares ||
            this.state.isLgViewportUp === null
        ) {
            return <LoadingPage />;
        }
        const isLgViewportUp = !!this.state.isLgViewportUp;
        const viewportZoom = isLgViewportUp ? 12.5 : 13;

        return (
            <div>
                <Container fluid>
                    <Row className="page-body">
                        <Col md={12} lg={7} className="page-map">
                            <Map
                                zoom={viewportZoom}
                                lat={this.state.mapLat}
                                lng={this.state.mapLng}
                                layers={{
                                    "Arrondissement": arrondissementsOverlay(this.state.geojsonData),
                                    "Photos available": densityOverlay(this.state.mapData, this.selectMapSquare),
                                }}
                                visibleLayers={["Photos available", "Arrondissement"]}
                                layerSelectVisible={true}
                                scrollWheelZoom={isLgViewportUp}
                            />
                        </Col>
                        <Col md={12} lg={5} className="m-0 p-0 min-vh-100">
                            <Container>
                                <Row>
                                    <Col lg={1} />
                                    <Col lg={11} className="p-0">
                                        {this.state.mapSquare ? (
                                            <>
                                                <TitleDecoratorContainer
                                                    title={`Map Square ${this.state.mapSquare}`}
                                                />

                                                <button
                                                    href={"#"}
                                                    className="small mb-4"
                                                    onClick={() => {
                                                        this.returnToMap();
                                                    }}
                                                >
                                                    &larr; Return
                                                </button>

                                                <MapSquareContent
                                                    mapSquare={this.state.mapSquare}
                                                    photos={this.state.photos}
                                                />
                                            </>
                                        ) : (
                                            <>
                                                <TitleDecoratorContainer title="Map" />
                                                <p>
                                                    In order to document the entire city, and not just its most touristy or photogenic neighborhoods,
                                                    the organizers of “This was Paris in 1970” divided up the city in 1755 squares and assigned
                                                    participants to document a square. Each square measured 250m by 250m. Because there were
                                                    more participants than squares, many contain documentation by multiple people. Squares that
                                                    contain no photos here were likely captured in black-and-white prints, which are available at the
                                                    BHVP in Paris.
                                                </p>
                                                <p>
                                                    Click on a square to see photos taken there.
                                                </p>

                                            </>
                                        )}
                                    </Col>
                                </Row>
                            </Container>
                        </Col>
                    </Row>
                </Container>
            </div>
        );
    }
}

MapPage.propTypes = {
    arrondissement_data: PropTypes.string,
};

export default MapPage;
