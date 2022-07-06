import React from "react";
import * as PropTypes from "prop-types";

import Navbar from "../../components/Navbar";
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
            selectedPhoto: 0
        };
    }

    async componentDidMount() {
        try {
            const response = await fetch(`/api/photographer/${this.props.photographerNumber}/`);
            if (!response.ok) {
                this.setState({loading: false});
            } else {
                const photographerData = await response.json();
                this.setState({
                    photographerData,
                    loading: false
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
            photos
        } = this.state.photographerData;

        const currentPhoto = photos[this.state.selectedPhoto];
        const squareCoords = currentPhoto.map_square_coords;
        const mapSquareBounds = [
            [squareCoords.lat, squareCoords.lng],
            [squareCoords.lat - MAPSQUARE_HEIGHT, squareCoords.lng - MAPSQUARE_WIDTH]
        ];

        return (<>
            <Navbar/>
            <div className="page row">
                <div className="image-view col-12 col-lg-6">
                    <div className="col-6">
                        <h3 style={{paddingTop: "1em"}}><strong>Photographer Profile</strong></h3>
                        <h1>{name}</h1>
                        <h5><strong>Number:</strong>{" " + number}</h5>
                        <h5><strong>Recorded Sex:</strong></h5>
                        <h5><strong>Address:</strong></h5>
                        <br/>
                        <p>
                            Lorem ipsum dolor sit amet, consectetur adipiscing
                            elit, sed do eiusmod tempor incididunt ut labore
                            et dolore magna aliqua. Ut enim ad minim veniam,
                            quis nostrud exercitation ullamco laboris nisi
                            ut aliquip ex ea commodo consequat. Duis aute
                            irure dolor in reprehenderit in voluptate velit
                            esse cillum dolore eu fugiat nulla pariatur.
                            Excepteur sint occaecat cupidatat non proident,
                            sunt in culpa qui officia deserunt mollit anim id
                            est laborum.
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
