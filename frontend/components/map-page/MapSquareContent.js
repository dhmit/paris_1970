import React from "react";
import * as PropTypes from "prop-types";
import {PhotoViewer} from "../../components/PhotoViewer";
import {Row, Col} from "react-bootstrap";
import Loading from "../Loading";

export class MapSquareContent extends PhotoViewer {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <>
                {this.props.photos.length ? (
                    <>
                        <Row>
                            <Col className={"p-0"}>
                                <div className="formatting-photos">
                                    <ul className={"list-inline p-0"}>
                                        {this.getPhotoGrid(this.props.photos, {
                                            photoSize: [240, 160],
                                            className: "example-photo",
                                        })}
                                    </ul>
                                </div>
                            </Col>
                        </Row>
                    </>
                ) : (
                    <Loading />
                )}
            </>
        );
    }
}

MapSquareContent.propTypes = {
    mapSquare: PropTypes.number,
    photos: PropTypes.array,
    photographers: PropTypes.string,
};

export default MapSquareContent;
