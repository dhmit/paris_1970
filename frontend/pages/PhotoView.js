import React from "react";
import * as PropTypes from "prop-types";

import PhotoViewer from "../components/PhotoViewer";
import LoadingPage from "./LoadingPage";
import ParisMap, {MAPSQUARE_HEIGHT, MAPSQUARE_WIDTH} from "../components/ParisMap";
import {Rectangle} from "react-leaflet";

import {Dropdown, OverlayTrigger, Popover, Modal} from "react-bootstrap";
import ExpandIcon from "../images/expand.svg";
import QuestionIcon from "../images/question.svg";
import TitleDecoratorContainer from "../components/TitleDecoratorContainer";
import { Trans, withTranslation } from "react-i18next";

const TURQUOISE = "#20CCD7";
// const NUM_PHOTOGRAPHERS = 72;


class BasePhotoView extends PhotoViewer {
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

    sortPhotos = (event) => {
        const analysisName = event.target.innerText;
        const newPhotoData = this.state.photoData;
        const images = (
            "photo_similarity.resnet18_cosine_similarity" in newPhotoData.analyses
                ? newPhotoData.analyses["photo_similarity.resnet18_cosine_similarity"]
                : []
        );
        images.sort((a, b) => {
            const valueA = a["analyses"][analysisName];
            const valueB = b["analyses"][analysisName];
            if (valueA < valueB) {
              return 1;
            }
            if (valueA > valueB) {
              return -1;
            }
            return 0;
        });
        newPhotoData.analyses["photo_similarity.resnet18_cosine_similarity"] = images;
        this.setState({photoData: newPhotoData});
    };

    render() {
        if (this.state.loading) {
            return <LoadingPage/>;
        }
        if (!this.state.photoData) {
            return (<h1><Trans
                i18nKey='PhotoView.photoNotFound'
                values={{ photoId: window.location.pathname.split("/")[2] }}
            /></h1>);
        }
        const {
            alt,
            map_square_number: mapSquareNumber,
            analyses,
            map_square_coords: squareCoords
        } = this.state.photoData;

        const tag_list = this.props.photoTags ? this.props.photoTags : [];

        const mapSquareBounds = [
            [squareCoords.lat || 0, squareCoords.lng || 0],
            [squareCoords.lat || 0 - MAPSQUARE_HEIGHT, squareCoords.lng || 0 - MAPSQUARE_WIDTH]
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
                            {this.props.t('PhotoView.PHOTO')}
                        </button>
                        <button
                            className={"side-button"}
                            style={{backgroundColor: this.state.displaySide === "slide" ? TURQUOISE : "white"}}
                            onClick={() => this.changeSide("slide")}>
                            {this.props.t('PhotoView.SLIDE')}
                        </button>
                    </div>
                    <div className="similar-photos-header">
                        <div className="similar-photos-title">
                            <h4>{this.props.t('PhotoView.similarPhotos')}</h4>
                            <OverlayTrigger
                                trigger="hover"
                                placement="right"
                                overlay={
                                    <Popover>
                                        <Popover.Body>                                            
                                            {this.props.t('PhotoView.similarPhotosHelp')}
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
                                {this.props.t('PhotoView.sortBy')}
                            </Dropdown.Toggle>

                            <Dropdown.Menu>
                                {
                                    Object.keys(analyses)
                                    .map(
                                        (analysisName, k) =>
                                            <Dropdown.Item key={k} onClick={this.sortPhotos}>
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
                                `Photo: ${photo["number"]}, ` +
                                `Similarity: ${photo["analyses"]["photo_similarity.resnet18_cosine_similarity"]}`,
                            hrefFunc: (k, photo) =>
                                `/photo/${photo.map_square_number}/${photo.folder}/${photo.number}/`
                        }
                    )}
                </div>
                <div className="image-info col-12 col-lg-6 col-md-4">
                    <TitleDecoratorContainer title={this.props.t('PhotoView.detailsHeader')}/>
                    {this.props.photographer_name
                        ? <><h6>{this.props.t('PhotoView.PHOTOGRAPHER')}</h6>
                            <p>
                                <a href={`/photographer/${this.props.photographer_number}/`}
                                   className={"photo-link"}>
                                    {this.props.photographer_name}
                                </a>
                                <br/>
                                {/* <span><strong>#23</strong></span> out of <span>
                                <a href={`/photographer/${this.props.photographer_number}/`}
                                   className={"photo-link"}>{NUM_PHOTOGRAPHERS}</a></span> in collection */}
                            </p></>
                        : <>{this.props.photographer_name} {this.props.photographer_number}</>
                    }

                    <div className="tags-container">
                        <h6>{this.props.t('PhotoView.TAGS')}</h6>
                        <OverlayTrigger
                            trigger="hover"
                            placement="right"
                            overlay={
                                <Popover>
                                    <Popover.Body>
                                        {this.props.t('PhotoView.TAGSHelp')}
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
                            ? tag_list.map((word) => {
                                let translatedTag = this.props.t(`global.objectTags.${word}`);
                                return <li className="list-inline-item single-tag" key={`tag-${translatedTag}`}>
                                    <a className="btn btn-secondary tag-button" key={`${translatedTag}-tag`}
                                       href={`/tag/${translatedTag}/`}>
                                        {translatedTag}
                                    </a>
                                </li>;
                            })
                            : <li>{this.props.t('PhotoView.noTags')}</li>
                        }
                    </ul>
                    <br/>

                    <h6>{this.props.t('PhotoView.LOCATION')}</h6>

                    <ParisMap className="single-photo-map"
                        lat={squareCoords.lat - MAPSQUARE_HEIGHT / 2}
                        lng={squareCoords.lng - MAPSQUARE_WIDTH / 2}
                        zoom={15}
                        t={this.props.t}
                        layers={{
                            mapSquare: <Rectangle
                                className="current-map-square"
                                key={mapSquareNumber}
                                bounds={mapSquareBounds}
                            />
                        }}
                    />
                    <b>
                        {this.props.t('global.mapSquare')} <span><a className="photo-link" href={`/map_square/${mapSquareNumber}`}>{mapSquareNumber}</a> </span>
                        <br/>
                    </b>
                </div>
            </div>
        </div>);
    }
}

BasePhotoView.propTypes = {
    photoNumber: PropTypes.number,
    folderNumber: PropTypes.number,
    mapSquareNumber: PropTypes.number,
    photo_dir: PropTypes.string,
    photographer_name: PropTypes.string,
    photographer_number: PropTypes.number
};

export const PhotoView = withTranslation()(BasePhotoView);
