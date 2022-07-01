import React from "react";
import PropTypes from "prop-types";
import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";
import {Container, Row, Col, Image} from "react-bootstrap";
import {Map} from "../Home";
import LoadingPage from "../LoadingPage";
import Logo from "../../components/Logo";

function MapPageEntryLogo(props){
    return <h1>Map</h1>;
}

class MapPage extends React.Component {
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

        return (<div>
                <Navbar/>
                <Container fluid>
                    <Row className="page-body">
                        <Col sm={2} md={7} className="m-0 p-0 min-vh-100" id="map-box"><Map mapData={this.state.mapData} /></Col>
                        <Col sm={2} md={5} className="m-0 p-0 min-vh-100" id="info-text">
                            <MapPageEntryLogo/>
                            <p>This is a small paragraph about the division of Paris into however many map squares for
                                this competition + other information about the format of the competition relevant to
                                interpreting this map. <br/><br/> Click on a square to learn more about it and see all the photos
                                taken in it!
                            </p>
                            <Logo id="site-logo" top={0} left={0}/>
                        </Col>
                    </Row>
                </Container>
            </div>
        );
    }

}

export default MapPage;
