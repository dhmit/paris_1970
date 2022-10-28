import React from "react";
import {Row, Col, Container} from "react-bootstrap";

//Images
import Map_Page from "../images/featured/map page.png";
import Walking_Man from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_078.jpg";
import Car from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_008.jpg";
import Staring_Man from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_024.jpg";
import Roof from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_002.jpg";
import Neighbourhood from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_012.jpg";
import House from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_030.jpg";


const randomMapImages = [Walking_Man, Car, Neighbourhood];

const randomContextImages = [Staring_Man, Roof, House];

function HomeSections() {

    return (
        <Container fluid id="home-sections" className="section">
            <a href="/photographers/">
                <Row className="photo-archive"
                    style={{
                        height: 475
                    }}>
                    <Col xs={8} sm={4} className="home-section-text">
                        <h5>Photography Archive:Explore Photos</h5>
                        <p>Capture a time of change in the city</p>
                        <span className="large-arrow d-none d-md-block d-lg-block">&#10230;</span>
                        <i className="bi bi-chevron-right"/>
                    </Col>
                    { <Col xs={4} sm={8} className="home-section-photo" 
                         style={{
                        backgroundImage: `url(${randomMapImages[Math.floor(Math.random() * randomMapImages.length)]})`,
                        backgroundRepeat: "no-repeat",
                        backgroundSize: 960
                        
                        }}>
                    </Col> }
                </Row>
            </a>

            <a href="/map/">
                <Row className="map-section"
                    style={{
                        height: 475
                    }}>
                    <Col xs={4} xxl={8} className="home-section-photo"
                         style={{backgroundImage: `url(${Map_Page})`}}/>
                    <Col xs={8} xxl={4} className="home-section-text">
                        <h5>Map Squares</h5>
                        <p>Capture a time of change in the city</p>
                        <span className="large-arrow d-none d-md-block d-lg-block">&#10230;</span>
                        <i className="bi-mid bi-chevron-left"/>
                    </Col>
                </Row>
            </a>

            <a href="/about/">
                <Row className="context"
                    style={{
                        height: 475
                    }}>
                    <Col xs={8} xxl={4} className="home-section-text">
                        <h5>Context:Paris 1970 photo contest</h5>
                        <p>Capture a time of change in the city</p>
                        <span className="large-arrow d-none d-md-block d-lg-block">&#10230;</span>
                        <i className="bi bi-chevron-right"/>
                    </Col>
                    <Col xs={4} xxl={8} className="home-section-photo"
                         style={{
                             backgroundImage: `url(${randomContextImages[Math.floor(
                                 Math.random() * randomContextImages.length)]})`,
                             filter: "grayscale(100%)",
                             backgroundRepeat: "no-repeat",
                             backgroundSize: 960
                            
                         }}>
                    </Col>
                </Row>
            </a>

        </Container>
    );
}

export default HomeSections;
