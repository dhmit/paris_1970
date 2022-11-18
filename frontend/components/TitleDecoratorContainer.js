import React from "react";
import * as PropTypes from "prop-types";
import {Col, Container, Row} from "react-bootstrap";
// import TitleDecorator from "../images/logos/title_decorator.svg";
import TitleDecoratorURL from "../images/logos/title_decorator.svg?url";

/* import TitleDecorator from "./TitleDecorator"; */

export class TitleDecoratorContainer extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const headerStyle = {
            background: `url(${TitleDecoratorURL})`,
            backgroundRepeat: `no-repeat`,
            width: 221,
            height: 55,
            marginLeft:35,
            paddingTop: 22,
            paddingLeft: 20
            
        };

        return (
            <Container className="p-0 title-decorator-container">
                <Row className="p-0">
                    <Col className="p-0">
                        {/* <TitleDecorator 
                            id="site-decorator"
                            top={22} left={-1.5} width={221} height={55}             
                            decorator_type={"title-decorator"}/>  */}
                                         
                        {/* <img src={} />  */}
                        <h2 style={headerStyle}> {this.props.title}</h2>
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


