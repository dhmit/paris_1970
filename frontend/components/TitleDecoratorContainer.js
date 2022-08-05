import React from "react";
import * as PropTypes from "prop-types";
import {Col, Container, Row} from "react-bootstrap";

import TitleDecorator from "./TitleDecorator";

export class TitleDecoratorContainer extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Container className="p-0 title-decorator-container">
                <Row className="p-0">
                    <Col className="p-0">
                        <TitleDecorator id="site-decorator" top={22} left={-1.5}
                                        decorator_type={"title-decorator"}/>
                        <h2>{this.props.title}</h2>
                    </Col>
                </Row>
            </Container>
        );
    }
}

TitleDecoratorContainer.propTypes = {
    title: PropTypes.string
};


export default TitleDecoratorContainer;


