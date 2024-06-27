import React from "react";
import * as PropTypes from "prop-types";

import {Rectangle} from "react-leaflet";

import PhotoViewer from "../components/PhotoViewer";
import LoadingPage from "./LoadingPage";
import ParisMap, {MAPSQUARE_HEIGHT, MAPSQUARE_WIDTH} from "../components/ParisMap";
import { Trans, withTranslation } from "react-i18next";


class BasePhotographerView extends PhotoViewer {

    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photographerData: null,
            selectedPhoto: null
        };
    }

    async componentDidMount() {
        try {
            const response = await fetch(`/api/photographer/${this.props.photographerNumber}/`);

            // TODO(ra): This looks like it was temporary progress code. Needs to be replaced by fetching
            // a real photo by the photographer.
            const selected = await fetch("/api/photo/120/1/1");
            if (!response.ok) {
                this.setState({loading: false});
            } else {
                const photographerData = await response.json();
                const selectedPhoto = await selected.json();
                this.setState({
                    photographerData,
                    loading: false,
                    selectedPhoto
                });

            }
        } catch (e) {
            console.log(e);
        }
    }

    onPhotoClick(photoKey) {
        this.setState({selectedPhoto: photoKey});
    }

    render() {
        if (this.state.loading) {
            return (<LoadingPage/>);
        }
        if (!this.state.photographerData) {
            return (<Trans
                i18nKey='Photographer.notInDB'
                values={{ photographerNum: this.props.photographerNumber }}
            />);
        }
        const {
            name,
            number,
            photos,
            recorded_sex,
            approx_loc
        } = this.state.photographerData;

        // const currentPhoto = photos[this.state.selectedPhoto];
        const currentPhoto = this.state.selectedPhoto;
        const squareCoords = currentPhoto.map_square_coords;
        const mapSquareBounds = [
            [squareCoords.lat, squareCoords.lng],
            [squareCoords.lat - MAPSQUARE_HEIGHT, squareCoords.lng - MAPSQUARE_WIDTH]
        ];

        return (<>
            <div className="page row">
                <div className="image-view col-12 col-lg-6">
                    <div className="col-10">
                        <h5 style={{
                            paddingTop: "1em",
                            fontSize: "28px"
                        }}><strong>{this.props.t("Photographer.profile")}</strong></h5>
                        <h1 className="photographer-name">{name}</h1>
                        <div><strong>{this.props.t("Photographer.number")}</strong>{": " + number}</div>
                        <div><strong>{this.props.t("Photographer.sex")}</strong>{": " + (
                            recorded_sex ? recorded_sex : this.props.t("Photographer.noRecord")
                        )}</div>
                        <div><strong>{this.props.t("Photographer.address")}</strong>{": " + (
                            approx_loc ? approx_loc : this.props.t("Photographer.noRecord")
                        )}</div>
                        <br/>
                        <p><Trans
                            i18nKey='Photographer.photosTaken'
                            values={{ name: name, numPhotos: photos.length }}
                        /></p>
                    </div>
                    <br/>
                    <h6>{this.props.t("Photographer.activity")}</h6>
                    <ParisMap
                        className="single-photo-map"
                        lat={squareCoords.lat - MAPSQUARE_HEIGHT / 2}
                        lng={squareCoords.lng - MAPSQUARE_WIDTH / 2}
                        zoom={17}
                        layers={{
                            "Map Square": <Rectangle
                                className="current-map-square"
                                key={currentPhoto.map_square_number}
                                bounds={mapSquareBounds}
                            />
                        }}
                    />
                </div>
                <div className="image-info col-12 col-lg-6">
                    <div className="photo-container">
                        <img
                            className="current-photo"
                            src={this.getSource(currentPhoto, this.state.displaySide)}
                            alt={currentPhoto.alt}
                        />
                    </div>
                    {this.getPhotoSlider(
                        photos,
                        {
                            "className": "slider-photo",
                            "hrefFunc": (_k, _photo) => "",
                            "onClickFunc": (k, _) => () => this.onPhotoClick(k)
                        }
                    )}
                </div>
            </div>
        </>);
    }
}

BasePhotographerView.propTypes = {
    photographerNumber: PropTypes.number,
    photo_dir: PropTypes.string
};

export const PhotographerView = withTranslation()(BasePhotographerView);