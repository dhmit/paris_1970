import React from "react";
import {Container, Row, Col} from "react-bootstrap";
import Map, {MAPSQUARE_HEIGHT, MAPSQUARE_WIDTH} from "../../components/ParisMap";
import LoadingPage from "../LoadingPage";
import Logo from "../../components/Logo";
import Legend from "../../components/Legend";
import {GeoJSON, Popup, Rectangle} from "react-leaflet";
import * as PropTypes from "prop-types";

function MapPageEntryLogo() {
    return (<div>
            <Container id="map-page-title">
                <Row>
                    <Col>
                        <Logo id="site-logo" top={22} left={-1.5} logo_type={"title-logo"}/>
                        <h2 className="page-title">Map</h2>
                    </Col>
                </Row>
            </Container>
        </div>
    );
}

function MapSquareList(props) {
    //Given an arrondissiment, only keeps the map squares that actually contain photos
    const mapSquareNumbers = props.arrondissementData[props.arrondissementNumber - 1]["map_square_numbers"].filter(
        number => props.filledMapSquares.has(number));

    if (mapSquareNumbers.length === 0) {
        return <span>No Map Squares!</span>;
    }

    //Returns a comma delimited list of the map square numbers in a arrondissement. Each number
    //links to corresponding map page
    const displayedMapSquares = mapSquareNumbers.map((map_square_number, i) => {
        const link = "/map_square/" + map_square_number + "/";
        return (<span key={map_square_number}>
                        <a href={link} className="info-list-link">{map_square_number}</a>
            {mapSquareNumbers[i + 1] ? ", " : ""}
                </span>);
    });

    return (<span>{displayedMapSquares}</span>);
}

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

class MapPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mapData: null,
            geojsonData: null
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
        try {
            const geojsonResponse = await fetch("/api/arrondissements_geojson/");
            const geojsonData = await geojsonResponse.json();

            //Fetches the data set containing which map squares belong to which arrondissement
            const mapSquareDataResponse = await fetch("/api/arrondissements_map_squares/");
            const mapSquareData = await mapSquareDataResponse.json();
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
                arrondissementData: mapSquareData["arrondissements"],
                geojsonData: geojsonData["features"],
                loading: false
            });
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        if (!this.state.mapData || !this.state.arrondissementData || !this.state.filledMapSquares) {
            return (<LoadingPage/>);
        }

        return (<div>
                <Container fluid className="page-style">
                    <Row className="page-body">
                        <Col md={12} lg={7} className="m-0 p-0 min-vh-100" id="map-box">
                            <Map className="page-map"
                                 zoom={13}
                                 layers={{
                                     "Photo Density": densityOverlay(this.state.mapData),
                                     "Arrondissements": arrondissementsOverlay(this.state.geojsonData)
                                 }}
                                 visibleLayers={["Photo Density"]}
                                 layerSelectVisible={true}/>
                        </Col>
                        <Col md={12} lg={5} className="m-0 p-0 min-vh-100">
                            <Container>
                                <Row>
                                    <Col lg={1}></Col>
                                    <Col lg={9}>
                                        <MapPageEntryLogo/>

                                        <p>
                                            This is a small paragraph about the division of Paris
                                            into however
                                            many map squares for this competition + other
                                            information about
                                            the format of the competition relevant to interpreting
                                            this map.
                                            <br/><br/> Click on a square to learn more about it and
                                            see all the
                                            photos taken in it!
                                        </p>

                                        <p className="info-header-link">Arrondissement 4</p>

                                        <p className="info-text">
                                            Map Squares: <MapSquareList
                                            arrondissementData={this.state.arrondissementData}
                                            arrondissementNumber={4}
                                            filledMapSquares={this.state.filledMapSquares}/>
                                        </p>

                                        <p className="info-text-small">
                                            Arrondissement 4 is known for being a cool place with
                                            many historical
                                            sites such as the Mickey Mouse clubhouse. Notable
                                            locations and events
                                            include this and that and these as well.
                                        </p>

                                        <p className="info-header-link">Arrondissement 19</p>

                                        <p className="info-text"> Map Squares: <MapSquareList
                                            arrondissementData={this.state.arrondissementData}
                                            arrondissementNumber={19}
                                            filledMapSquares={this.state.filledMapSquares}/>
                                        </p>

                                        <p className="info-text-small">
                                            Arrondissement 19 is known for being a cool place with
                                            many historical
                                            sites such as the Mickey Mouse clubhouse. Notable
                                            locations and events
                                            include this and that and these as well.
                                        </p>
                                        {
                                            //Eventually all arrondissement info will
                                            // be in separate functional component.
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

MapSquareList.propTypes = {
    arrondissementData: PropTypes.array,
    arrondissementNumber: PropTypes.number,
    filledMapSquares: PropTypes.object
};

export default MapPage;
