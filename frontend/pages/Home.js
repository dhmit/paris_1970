import React from "react";
import {Modal, Button, Row, Col} from "react-bootstrap";


//Images
import Car from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_008.jpg";
import Logo_Gif from "../images/gif/rec-animation-english---Copy.gif";
import Map_Page from "../images/featured/map page.png";
import Staring_Man from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_024.jpg";
import Walking_Man from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_078.jpg";
// import House from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_030.jpg";
// import Roof from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_002.jpg";
// import Neighbourhood from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_012.jpg";



const WorkInProgressModal = ({showModal, handleClose}) => {
    return (
        <Modal show={showModal} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Pardon Our Dust!</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <p>
                    <strong>This was Paris in 1970</strong> is a project by
                    the <a href = "https://digitalhumanities.mit.edu/">MIT
                    Digital Humanities Lab</a> in collaboration with <a href =
                    "https://history.mit.edu/people/catherine-clark/">Catherine
                    Clark</a>, Associate Professor of History and French Studies
                    at MIT and Director of MIT Digital Humanities.
                </p>
                <p>
                    This project is still under construction and contains
                    student work, so there may be features that are
                    currently incomplete or inaccurate.
                </p>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    );
};



export class HomePage extends React.Component {
    state = {
        showModal: false
    };

    handleClose = () => this.setState({showModal: false});

    render() {

        return (<>
            <WorkInProgressModal showModal={this.state.showModal} handleClose={this.handleClose} />

            <section className="home-hero-section">
                <div className="main-section" style={{backgroundImage: `url(${Car})`}}>
                    <img src={Logo_Gif} alt="Paris Logo"/>
                    <div className="scroll-down">
                        Scroll down to enter
                    </div>
                </div>
            </section>

            <section className="home-sections">
                <a href="/explore/">
                    <Row className="section-row photo-archive gx-0">
                        <Col sm={4} className="home-section-text">
                            <h2 className="h4">Photography Archive: Explore Photos</h2>
                            <p>Capture a time of change in the city</p>
                            <span className="large-arrow right">⟶</span>
                        </Col>
                        <Col sm={8} className="home-section-photo" style={{ backgroundImage: `url(${Walking_Man})` }} />
                    </Row>
                </a>

                <a href="/map/">
                    <Row className="section-row map-section gx-0">
                        <Col sm={8} className="home-section-photo"
                            style={{
                                backgroundImage: `url(${Map_Page})`,
                            }}
                        />
                        <Col sm={4} className="home-section-text">
                            <h2 className="h4">Map Squares</h2>
                            <p>Capture a time of change in the city</p>
                            <span className="large-arrow left">⟵</span>
                        </Col>
                    </Row>
                </a>

                <a href="/blog/">
                    <Row className="section-row context gx-0">
                        <Col xs={8} sm={4} className="home-section-text">
                            <h2 className="h4">Context: Paris 1970 photo contest</h2>
                            <p>Capture a time of change in the city</p>
                            <span className="large-arrow right">⟶</span>
                        </Col>
                        <Col xs={4} sm={8} className="home-section-photo"
                            style={{
                                backgroundImage: `url(${Staring_Man})`,
                            }}
                        />
                    </Row>
                </a>

                <a href="/about/">
                    <Row className="section-row map-section gx-0">
                        <Col sm={8} className="home-section-photo"
                            style={{
                                backgroundImage: `url(${Map_Page})`,
                            }}
                        />
                        <Col sm={4} className="home-section-text">
                            <h2 className="h4">About the Project</h2>
                            <p>Learn about MIT Prof. Catherine Clark and the Digital Humanities Lab</p>
                            <span className="large-arrow left">⟵</span>
                        </Col>
                    </Row>
                </a>


            </section>

        </>);
    }
}
