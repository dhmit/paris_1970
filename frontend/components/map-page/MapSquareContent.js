import React from "react";
import * as PropTypes from "prop-types";
import PhotoViewer from "../../components/PhotoViewer";
import {Row, Col} from "react-bootstrap";


export class MapSquareContent extends PhotoViewer {
    constructor(props) {
        super(props);
    }

    render() {
        return (<>
            {this.props.photos.length

                ? (<>
                    <h6 className={"text-uppercase"}>Example photos</h6>
                    <Row>
                        <Col sm={12} lg={9} className={"p-0"}>
                            <ul className={"list-inline p-0"}>{
                                this.getPhotoGrid(this.props.photos, {
                                    "photoSize": [120, 120],
                                    "className": "example-photo"
                                })
                            }
                            </ul>
                        </Col>
                    </Row>
                    <Row>
                        <Col className="d-inline-block p-0">
                            <a className={"link"}
                               href={"/map_square/" + this.props.mapSquare}>
                                Go to map square
                            </a>
                        </Col>
                    </Row>
                </>)
                : <></>
            }
            {this.props.photographers.length ? <>
                <h6 className={"text-uppercase"}>Photographers</h6>
            </> : <></>}
        </>);
    }
}

MapSquareContent.propTypes = {
    mapSquare: PropTypes.number,
    photos: PropTypes.array,
    photographers: PropTypes.array,
    photoDir: PropTypes.string
};

export default MapSquareContent;
