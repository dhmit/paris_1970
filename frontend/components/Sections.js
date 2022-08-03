import React from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import "../scss/sections.scss";

// images
import Map_Page from "../images/featured/map page.png";
import Walking_Man from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_078.jpg";
import Car from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_008.jpg";
import Staring_Man from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_024.jpg";
import Roof from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_002.jpg";
import Neighbourhood from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_012.jpg";
import House from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_030.jpg";


const randomMapImages = [Walking_Man, Car, Neighbourhood];

const randomContextImages = [Staring_Man, Roof, House];

function Sections() {
    return (
        <Container fluid>
            <a href= '#photo'>
                <Row className="photo-archive">
                     <Col xs={8} xxl={4} className="text">
                         <h5>Photography Archive:Explore Photos</h5>
                        <p>Capture a time of change in the city</p>
                       <span className="arrow">&#10230;</span>

                    </Col>
                    <Col xs={4} xxl={8} className="photo" style={{
                        backgroundImage: `url(${randomMapImages[Math.floor(Math.random() * randomMapImages.length)]})`
                    }}>
                    </Col>
                </Row>
            </a>

            <a href= '#map'>
                <Row className="map-section">
                    <Col xs={4} xxl={8} className="photo" style={{backgroundImage: `url(${Map_Page})`}}/>
                    <Col xs={8} xxl={4} className="text">
                        <h5>Map Squares</h5>
                        <p>Capture a time of change in the city</p>
                        <span className="arrow">&#10230;</span>
                    </Col>
                </Row>
            </a>

            <a href= '#context'>
                <Row className="context">
                    <Col xs={8} xxl={4} className="text">
                        <h5>Context:Paris 1970 photo contest</h5>
                        <p>Capture a time of change in the city</p>
                        <span className="arrow">&#10230;</span>
                    </Col>
                    <Col xs={4} xxl={8} className="photo"
                         style={{backgroundImage: `url(${randomContextImages[Math.floor(Math.random() * randomContextImages.length)]})`,filter:"grayscale(100%)"
                    }}>
                    </Col>
                </Row>
            </a>

        </Container>
    );
}

export default Sections;
