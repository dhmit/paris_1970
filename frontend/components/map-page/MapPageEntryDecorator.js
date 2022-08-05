import React from "react";
import * as PropTypes from "prop-types";
import {Col, Container, Row} from "react-bootstrap";
import TitleDecorator from "../TitleDecorator";

function MapPageEntryDecorator(props) {
    return (<div>
            <Container id="map-page-title">
                <Row>
                    <Col>
                        <TitleDecorator id="site-decorator" top={22} left={-1.5}
                                        decorator_type={"title-decorator"}/>
                        <h2>{props.title}</h2>
                    </Col>
                </Row>
            </Container>
        </div>
    );
}

MapPageEntryDecorator.propTypes = {
    title: PropTypes.string
};

export default MapPageEntryDecorator;
