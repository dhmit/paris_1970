import React from "react";
import * as PropTypes from "prop-types";

import PhotoViewer from "../../components/PhotoViewer";
import LoadingPage from "../LoadingPage";
import ParisMap, {MAPSQUARE_HEIGHT, MAPSQUARE_WIDTH} from "../../components/ParisMap";
import {Rectangle} from "react-leaflet";

import {Dropdown, OverlayTrigger, Popover, Modal} from "react-bootstrap";
import ExpandIcon from "../../images/expand.svg";
import QuestionIcon from "../../images/question.svg";
import TitleDecoratorContainer from "../../components/TitleDecoratorContainer";

const TURQUOISE = "#20CCD7";


export class PhotoView extends PhotoViewer {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photoData: null,
            displaySide: "photo",
            availableSides: [],
            view: 0,
            width: null,
            height: null,
            natWidth: null,
            natHeight: null,
            labels: null,
            mapData: null,
            prevLink: null,
            nextLink: null,
            showPhotoModal: false
        };
        this.onImgLoad = this.onImgLoad.bind(this);
        this.photoRef = React.createRef();
    }

    async componentDidMount() {
        const mapPhotoString = `${this.props.mapSquareNumber}/${this.props.folderNumber}/${this.props.photoNumber}/`;
        try {
            const apiURL = "/api/photo/" + mapPhotoString;
            const response = await fetch(apiURL);
            if (!response.ok) {
                this.setState({loading: false});
            } else {
                const photoData = await response.json();
                this.setState({
                    photoData,
                    loading: false
                });
            }
        } catch (e) {
            console.log(e);
        }
        try {
            const photoResponse = await fetch("/api/prev_next_photos/" + mapPhotoString);
            let prevNextPhotos = await photoResponse.json();
            prevNextPhotos = prevNextPhotos.map((photo) => {
                return photo ? `/photo/${photo.map_square_number}/${photo.number}/` : null;
            });
            this.setState({
                prevLink: prevNextPhotos[0],
                nextLink: prevNextPhotos[1],
                loading: false
            });
        } catch (e) {
            console.log(e);
        }
    }

    changeSide = (displaySide) => {
        this.setState({displaySide: displaySide});
    };

    onImgLoad({target: img}) {
        this.setState({
            width: img.clientWidth,
            height: img.clientHeight,
            natWidth: img.naturalWidth,
            natHeight: img.naturalHeight
        });
    }

    handleResize() {
        const img = this.photoRef.current;
        this.setState({
            height: img.getBoundingClientRect()["height"],
            width: img.getBoundingClientRect()["width"]
        });
    }

    render() {
        if (this.state.loading) {
            return (<LoadingPage/>);
        }
        if (!this.state.photoData) {
            return (<h1>
                Photo with id {window.location.pathname.split("/")[2]} is not in database.
            </h1>);
        }
        const {
            alt,
            map_square_number: mapSquareNumber,
            analyses,
            map_square_coords: squareCoords
        } = this.state.photoData;

        const tag_list = this.props.photoTags ? this.props.photoTags : [];

        const mapSquareBounds = [
            [squareCoords.lat, squareCoords.lng],
            [squareCoords.lat - MAPSQUARE_HEIGHT, squareCoords.lng - MAPSQUARE_WIDTH]
        ];

        // Resize SVG overlays on viewport resize
        window.addEventListener("resize", () => this.handleResize());

        // Close photo popup by pressing the Esc key
        window.addEventListener(
            "keydown",
            (e) => e.code === "Escape"
                ? this.setState({showPhotoModal: false})
                : null
        );

        const similarPhotos = (
            "photo_similarity.resnet18_cosine_similarity" in analyses
                ? analyses["photo_similarity.resnet18_cosine_similarity"]
                : []
        );

        return (<div className="page" id="photo-view">
            <br/>
            <Modal
                className="photo-modal"
                show={this.state.showPhotoModal}
                onHide={() => this.setState({showPhotoModal: false})}
                backdrop="static"
                keyboard={false}
                aria-labelledby="contained-modal-title-vcenter"
                fullscreen>
                <Modal.Header closeButton/>
                <Modal.Body className="photo-modal-body">
                    <img
                        className="photo-popup"
                        alt={this.state.photoData.alt}
                        src={this.getSource(this.state.photoData)}
                    />
                </Modal.Body>
            </Modal>
            <div className="page row">
                <div className="image-view col-12 col-lg-6 col-md-8">
                    <div
                        className={this.state.displaySide === "slide" ? "image-box slide" : "image-box"}>
                        <img
                            className="image-photo position-top-left"
                            src={this.getSource(this.state.photoData, this.state.displaySide)}
                            alt={alt}
                            onLoad={this.onImgLoad}
                            ref={this.photoRef}
                        />
                    </div>
                    <div className={"center-btn mb-4"}>
                        <ExpandIcon
                            className="expand-icon"
                            onClick={() => this.setState({showPhotoModal: true})}
                        />
                        <button
                            className={"side-button"}
                            style={{backgroundColor: this.state.displaySide === "photo" ? TURQUOISE : "white"}}
                            onClick={() => this.changeSide("photo")}>
                            PHOTO
                        </button>
                        <button
                            className={"side-button"}
                            style={{backgroundColor: this.state.displaySide === "slide" ? TURQUOISE : "white"}}
                            onClick={() => this.changeSide("slide")}>
                            SLIDE
                        </button>
                    </div>
                    <div className="similar-photos-header">
                        <div className="similar-photos-title">
                            <h4>Similar Photos</h4>
                            <OverlayTrigger
                                trigger="hover"
                                placement="right"
                                overlay={
                                    <Popover>
                                        <Popover.Body>
                                            This is what similar photos are and how we generate
                                            them.
                                        </Popover.Body>
                                    </Popover>
                                }>
                                <button className="info-button">
                                    <QuestionIcon/>
                                </button>
                            </OverlayTrigger>
                        </div>
                        <Dropdown className="photo-sort-dropdown">
                            <Dropdown.Toggle className="photo-sort-dropdown-button"
                                             align="start">
                                Sort By...
                            </Dropdown.Toggle>

                            <Dropdown.Menu>
                                {
                                    Object.keys(analyses)
                                    .map(
                                        (analysisName, k) =>
                                            <Dropdown.Item key={k} href={`#/action-${k}`}>
                                                {analysisName}
                                            </Dropdown.Item>
                                    )
                                }
                            </Dropdown.Menu>
                        </Dropdown>
                    </div>
                    {this.getPhotoSlider(
                        similarPhotos,
                        {
                            className: "slider-photo",
                            titleFunc: (k, photo) =>
                                `Map Square: ${photo["map_square_number"]}, ` +
                                `Photo: ${photo["number"]}, Similarity: ${photo["similarity"]}`,
                            hrefFunc: (k, photo) => 
                                `/photo/${photo.map_square_number}/${photo.folder_number}/${photo.number}/`
                        }
                    )}
                </div>
                <div className="image-info col-12 col-lg-6 col-md-4">
                    <TitleDecoratorContainer title="Photograph Details"/>
                    {this.props.photographer_name
                        ? <><h6>PHOTOGRAPHER</h6>
                            <p>
                                <a href={`/photographer/${this.props.photographer_number}/`}
                                   className={"photo-link"}>
                                    {this.props.photographer_name}
                                </a>
                                <br/>
                                <span><strong>#23</strong></span> out of <span>
                                <a href={`/photographer/${this.props.photographer_number}/`}
                                   className={"photo-link"}>72</a></span> in collection
                            </p></>
                        : <>{this.props.photographer_name} {this.props.photographer_number}</>
                    }

                    <div className="tags-container">
                        <h6>TAGS</h6>
                        <OverlayTrigger
                            trigger="hover"
                            placement="right"
                            overlay={
                                <Popover>
                                    <Popover.Body>
                                        This is what a tag is and how we generate them.
                                    </Popover.Body>
                                </Popover>
                            }>
                            <button className={"info-button"}>
                                <QuestionIcon/>
                            </button>
                        </OverlayTrigger>
                    </div>
                    <ul className="list-inline list-tags">
                        {tag_list.length !== 0
                            ? tag_list.map((word) => (
                                <li className="list-inline-item single-tag" key={`tag-${word}`}>
                                    <a className="btn btn-secondary tag-button" key={`${word}-tag`}
                                       href={`/tag/${word}/`}>
                                        {word}
                                    </a>
                                </li>
                            ))
                            : <li>No tags to display for this photo.</li>
                        }
                    </ul>
                    <br/>

                    <h6>LOCATION</h6>

                    <ParisMap className="single-photo-map"
                        lat={squareCoords.lat - MAPSQUARE_HEIGHT / 2}
                        lng={squareCoords.lng - MAPSQUARE_WIDTH / 2}
                        zoom={15}
                        layers={{
                            mapSquare: <Rectangle
                                className="current-map-square"
                                key={mapSquareNumber}
                                bounds={mapSquareBounds}
                            />
                        }}
                    />
                    <b>
                        Map Square
                        <span>
                            <a className="photo-link"
                                href={`/map_square/${mapSquareNumber}`}
                            >{mapSquareNumber}</a>
                        </span>
                        <br/>
                        Arrondissement 17
                    </b>
                </div>
            </div>
        </div>);
    }
}

PhotoView.propTypes = {
    photoNumber: PropTypes.number,
    folderNumber: PropTypes.number,
    mapSquareNumber: PropTypes.number,
    photo_dir: PropTypes.string,
    photographer_name: PropTypes.string,
    photographer_number: PropTypes.number
};
