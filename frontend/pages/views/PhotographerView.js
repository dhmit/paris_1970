import React from "react";
import * as PropTypes from "prop-types";

import Footer from "../../components/Footer";
import PhotoViewer from "../../components/PhotoViewer";
import LoadingPage from "../LoadingPage";
import ParisMap, {MAPSQUARE_HEIGHT, MAPSQUARE_WIDTH} from "../../components/ParisMap";
import {Rectangle} from "react-leaflet";


export class PhotographerView extends PhotoViewer {

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
            const selected = await fetch("/api/photo/1554/70");
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
            return (<>
                Photographer number ${this.props.photographerNumber} is not in the database.
            </>);
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
                        <h5 style={{paddingTop: "1em", fontSize:"28px"}}><strong>Photographer Profile</strong></h5>
                        <h1 className="photographer-name">{name}</h1>
                        <div><strong>Number:</strong>{" " + number}</div>
                        <div><strong>Recorded Sex:</strong>{" " + (recorded_sex ? recorded_sex : "No" +
                            " record")}</div>
                        <div><strong>Address:</strong>{" " + (approx_loc ? approx_loc : "No" +
                            " record")}</div>
                        <br/>
                        <p>
                            {name} took a total of {photos.length} photos for the competition.
                        </p>
                    </div>
                    <br/>
                    <h6>MAP OF ACTIVITY</h6>
                    <ParisMap
                        className="single-photo-map"
                        lat={squareCoords.lat - MAPSQUARE_HEIGHT / 2}
                        lng={squareCoords.lng - MAPSQUARE_WIDTH / 2}
                        zoom={17}
                        layers={{
                            mapSquare: <Rectangle
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
                            "className": "photo slider-photo",
                            "hrefFunc": (_k, _photo) => "#",
                            "onClickFunc": (k, _) => () => this.onPhotoClick(k)
                        }
                    )}
                </div>
            </div>
            <Footer/>
        </>);
    }
}

PhotographerView.propTypes = {
    photographerNumber: PropTypes.number,
    photo_dir: PropTypes.string
};
