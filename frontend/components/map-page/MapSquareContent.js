import React from "react";
import * as PropTypes from "prop-types";
import {PhotoViewer, getValue} from "../../components/PhotoViewer";
import {Row, Col} from "react-bootstrap";

export class MapSquareContent extends PhotoViewer {
    constructor(props) {
        super(props);
    }

    getPhotographersGrid(photographerData, config = {}){
        
        const className = getValue(config, "className", "");
        const titleFunc = getValue(
            config,
            "titleFunc",
            (k, photographer) => `Map Square: ${photographer["map_square"]}` +
                `, Photographer: ${photographer["name"]}`
        );
        const hrefFunc = getValue(
            config,
            "hrefFunc",
            (k, photographer) => `/photographer/${photographer["number"]}/`
        );
        const onClickFunc = getValue(
            config, "onClickFunc", (_k, _photographer) => (_e) => {
            }
        );
        return photographerData.map((photographer, k) => {
            return (
                <li className={`default-photographer list-inline-item ${className}`}
                    key={k}
                    onClick={(e) => {
                        onClickFunc(k, photographer)(e);
                        window.open(hrefFunc(k, photographer), "_self");
                    }}>
                    <button type= "button" 
                        className="btn-secondary-blue"
                        title={titleFunc(k, photographer)}
                        href={hrefFunc(k, photographer)}
                        onClick={onClickFunc(k, photographer)}>
                            {photographer["name"]}
                    </button>
                </li>
            );
        });
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
                    
                </>)
                : <></>
            }
            {this.props.photographers.length 
            
                ? (<>
                <h6 className={"text-uppercase"}>Photographers</h6>
                    <Row>
                        <Col sm={12} lg={9} className={"p-1"}>
                            <ul className={"list-inline p-0"}>{
                                this.getPhotographersGrid(this.props.photographers
                                )
                            }
                            </ul>
                        </Col>
                    </Row>
                </>)
                : <></>
            }
            {
                    <Row>
                        <Col className="d-inline-block p-0">
                            <a className={"link"}
                               href={"/map_square/" + this.props.mapSquare}>
                                Go to map square
                            </a>
                        </Col>
                    </Row>
            }
        </>);
    }
}

MapSquareContent.propTypes = {
    mapSquare: PropTypes.number,
    photos: PropTypes.array,
    // photographers: PropTypes.array,
    photographers: PropTypes.string,
};

export default MapSquareContent;
