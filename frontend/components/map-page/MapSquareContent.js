import React from "react";
import * as PropTypes from "prop-types";
import {PhotoViewer} from "../../components/PhotoViewer";
import {Row, Col} from "react-bootstrap";

export class MapSquareContent extends PhotoViewer {
    constructor(props) {
        super(props);
    }

    getPhotographersGrid(
        photographerData,
        config = {
            className: "",
            titleFunc: (_key, photographer) =>
                `Map Square: ${photographer["map_square"]}, Photographer: ${photographer["name"]}`,
            hrefFunc: (_key, photographer) => `/photographer/${photographer["number"]}/`,
            onClickFunc: (_key, _photographer) => (_e) => {},
        }
    ) {
        const {className, titleFunc, hrefFunc, onClickFunc} = config;

        return photographerData.map((photographer, key) => {
            return (
                <li
                    className={`default-photographer list-inline-item ${className}`}
                    key={key}
                    onClick={(e) => {
                        onClickFunc(key, photographer)(e);
                        window.open(hrefFunc(key, photographer), "_self");
                    }}
                >
                    <button
                        type="button"
                        className="btn-secondary-blue"
                        title={titleFunc(key, photographer)}
                        href={hrefFunc(key, photographer)}
                        onClick={onClickFunc(key, photographer)}
                    >
                        {photographer["name"]}
                    </button>
                </li>
            );
        });
    }

    render() {
        return (
            <>
                {this.props.photos.length ? (
                    <>
                        <h6 className={"text-uppercase"}>Example photos</h6>
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
                    <></>
                )}
                {this.props.photographers.length ? (
                    <>
                        <h6 className={"text-uppercase"}>Photographers</h6>
                        <Row>
                            <Col className={"p-1"}>
                                <ul className={"list-inline p-0"}>
                                    {this.getPhotographersGrid(this.props.photographers)}
                                </ul>
                            </Col>
                        </Row>
                    </>
                ) : (
                    <></>
                )}
                {
                    <Row>
                        <Col className="d-inline-block p-0">
                            <a className={"link"} href={"/map_square/" + this.props.mapSquare}>
                                Go to map square
                            </a>
                        </Col>
                    </Row>
                }
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
