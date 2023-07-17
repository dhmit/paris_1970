import React from "react";
import HomeSections from "../components/HomeSections";
import Logo_Gif from "../images/gif/rec-animation-english---Copy.gif";
import Car from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_008.jpg";
import Arrows from "../images/icons/scroll_down.svg";
import {Modal, Button} from "react-bootstrap";


export class HomePage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            showModal: true
        };
    }

    render() {
        const handleClose = () => this.setState({showModal: false});

        return (<>
            <Modal show={this.state.showModal} onHide={handleClose}>
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

            <section>
                
                <div className="main-section">
                    <img src={Logo_Gif} alt="Paris Logo"/>
                    <img src={Car} className="background" alt="Background image: Car"/>
                </div>
                <div className = "see_below_text"> Scroll down to enter</div>
                <div className = "scroll_down">
                    <a className = "btn transparent_button" href="#home-sections"><Arrows/></a>
                </div>
                <HomeSections/>
            </section>
        </>);
    }
}
