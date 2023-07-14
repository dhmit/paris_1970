import React from "react";
import {Row, Col} from "react-bootstrap";
import DHLogo from "../images/logos/dh_logo.svg";
import MITLogo from "../images/logos/mit_logo.svg";
import MellonLogo from "../images/logos/mellon_logo.svg";

export class Footer extends React.Component {
    render() {
        return (
            // return to edit the footer's location
            <Row className={"mt-3 text-center footer fixed-bottom"}> 
                <Col>
                    <a href="https://digitalhumanities.mit.edu/">
                        <DHLogo height={"40px"}/>
                    </a>
                </Col>
                <Col>
                    <a href="https://www.mit.edu/">
                        <MITLogo height={"42px"}/>
                    </a>
                </Col>
                <Col>
                    <a href="https://www.mellon.org/">
                        <MellonLogo height={"50px"}/>
                    </a>
                </Col>
            </Row>
        );
    };
};

export default Footer;
