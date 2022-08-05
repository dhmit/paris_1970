import React from "react";
import * as PropTypes from "prop-types";

import {GeoJSON, Popup, Rectangle} from "react-leaflet";
import {Container, Row, Col} from "react-bootstrap";

import {debounce} from "../../common";

import Map, {MAPSQUARE_HEIGHT, MAPSQUARE_WIDTH} from "../../components/ParisMap";
import LoadingPage from "../LoadingPage";
import MapSquareList from "../../components/map-page/MapSquareList";
import MapSquareContent from "../../components/map-page/MapSquareContent";
import MapPageEntryDecorator from "../../components/map-page/MapPageEntryDecorator";


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
                        {// Shows map square numbers on each map square
                            // <Marker position={L.polygon(mapSquareBounds).getBounds().getCenter()}
                            //icon={L.divIcon({html: index})} />
                        }
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
            photographers: []
        };
        this.selectMapSquare = this.selectMapSquare.bind(this);
        this.updateViewport = this.updateViewport.bind(this);
        this.returnToMap = this.returnToMap.bind(this);
        this.arrondissementData = JSON.parse(this.props.arrondissement_data)["arrondissements"];
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
                loading: false
            });
        } catch (e) {
            console.log(e);
        }

        this.updateViewport();

        window.addEventListener("resize", debounce(() => this.updateViewport(), 250));
    }

    async selectMapSquare(mapSquare) {
        this.setState({mapSquare: mapSquare});
        this.state.mapData.map(ms => {
            if (ms.id === mapSquare) {
                return this.setState({
                    mapLat: ms.topLeftCoords.lat,
                    mapLng: ms.topLeftCoords.lng
                });
            }
        });
        const mapSquareDetails = await fetch("/api/map_square_details/" + mapSquare);
        const mapSquareDetailsJSON = await mapSquareDetails.json();
        this.setState({
            photos: mapSquareDetailsJSON.photos,
            photographers: mapSquareDetailsJSON.photographers
        });
    }

    updateViewport() {
        this.setState({isLgViewportUp: window.innerWidth > 992});
    }

    returnToMap() {
        this.setState({mapSquare: null});
    }

    render() {
        if (!this.state.mapData || !this.state.filledMapSquares ||
            this.state.isLgViewportUp === null) {
            return (<LoadingPage/>);
        }
        const isLgViewportUp = !!this.state.isLgViewportUp;
        const viewportZoom = isLgViewportUp ? 12.5 : 13;

        return (<div>
                <Container fluid>
                    <Row className="page-body">
                        <Col md={12} lg={7} className="page-map">
                            <Map zoom={viewportZoom}
                                 lat={this.state.mapLat}
                                 lng={this.state.mapLng}
                                 layers={{
                                     "Arrondissements": arrondissementsOverlay(this.state.geojsonData),
                                     "Photo Density": densityOverlay(this.state.mapData)
                                 }}
                                 visibleLayers={["Photo Density"]}
                                 layerSelectVisible={true}
                                 scrollWheelZoom={isLgViewportUp}/>
                        </Col>
                        <Col md={12} lg={5} className="m-0 p-0 min-vh-100">
                            <Container>
                                <Row>
                                    <Col lg={1}/>
                                    <Col lg={9} className="p-0">
                                        {this.state.mapSquare
                                            ? <>
                                                <a href={"#"}
                                                   className={"small"}
                                                   onClick={() => {
                                                       this.returnToMap();
                                                   }}>
                                                    &larr; Return
                                                </a>
                                                <MapPageEntryDecorator
                                                    title={`Map Square ${this.state.mapSquare}`}/>
                                                <MapSquareContent mapSquare={this.state.mapSquare}
                                                                  photos={this.state.photos}
                                                                  photographers={this.state.photographers}
                                                                  photoDir={this.props.photoDir}/>
                                            </>
                                            : <>
                                                <MapPageEntryDecorator title={"Map"}/>
                                                <p>
                                                    This is a small paragraph about the division of
                                                    Paris into however many map squares for this
                                                    competition + other information about
                                                    the format of the competition relevant to
                                                    interpreting this map.
                                                    <br/><br/> Click on a square to learn more about
                                                    it and see all the photos taken in it!
                                                </p>

                                                <p className="info-header-link">Arrondissement
                                                    13</p>

                                                <p className="info-text">
                                                    Map Squares: <MapSquareList
                                                    setSelectedMapSquare={this.selectMapSquare}
                                                    arrondissementData={this.arrondissementData}
                                                    arrondissementNumber={13}
                                                    filledMapSquares={this.state.filledMapSquares}/>
                                                </p>

                                                <p className="info-text-small">
                                                    Arrondissement 4 is known for being a cool place
                                                    with many historical sites such as the Mickey
                                                    Mouse clubhouse. Notable locations and events
                                                    include this and that and these as well.
                                                </p>

                                                <p className="info-header-link">Arrondissement
                                                    19</p>

                                                <p className="info-text">
                                                    Map Squares: <MapSquareList
                                                    setSelectedMapSquare={this.selectMapSquare}
                                                    arrondissementData={this.arrondissementData}
                                                    arrondissementNumber={19}
                                                    filledMapSquares={this.state.filledMapSquares}/>
                                                </p>

                                                <p className="info-text-small">
                                                    Arrondissement 19 is known for being a cool
                                                    place with many historical sites such as the
                                                    Mickey Mouse clubhouse. Notable locations and
                                                    events include this and that and these as well.
                                                </p>
                                            </>
                                        }

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
    photoDir: PropTypes.string
};

export default MapPage;
