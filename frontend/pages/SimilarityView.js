import React from "react";
import * as PropTypes from "prop-types";

import Footer from "../components/Footer";
import PhotoViewer from "../components/PhotoViewer";
import LoadingPage from "./LoadingPage";


/*
Creates a view to show the most similar photos for a photo given url with a number of photos
 */
export class SimilarityView extends PhotoViewer {
    constructor(props) {
        super(props);
        console.log(props);
        this.state = {
            loadingSimilar: true,
            loadingOriginal: true,
            similarPhotosData: null,
            originalPhotoData: null,
        };
    }

    async componentDidMount() {
        // Load original image
        try {
            const apiURL = "/api/photo/" +
                `${this.props.mapSquareNumber}/${this.props.folderNumber}/${this.props.photoNumber}/`;

            const response = await fetch(apiURL);
            if (!response.ok) {
                this.setState({loading: false});
            } else {
                const originalPhotoData = await response.json();
                this.setState({
                    originalPhotoData,
                    loadingOriginal: false
                });
            }
        } catch (e) {
            console.log(e);
        }

        // Load similar images
        const numSimilarPhotos = 40;
        try {
            const apiURL = "/api/similar_photos/" +
                `${this.props.mapSquareNumber}/${this.props.folderNumber}/${this.props.photoNumber}/` +
                `${numSimilarPhotos}/`;
            const response = await fetch(apiURL);
            if (!response.ok) {
                this.setState({loading: false});
            } else {
                const similarPhotosData = await response.json();
                this.setState({
                    similarPhotosData,
                    loadingSimilar: false
                });
            }
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        const loading = this.state.loadingSimilar || this.state.loadingOriginal;
        if (loading) return (<LoadingPage/>);

        if (!this.state.similarPhotosData) {
            return (<h1>
                Photo with id {window.location.pathname.split("/")[2]} is not in database.
            </h1>);
        }

        if (this.state.similarPhotosData.length === 0) {
            return (<h1>
                Photo with id {window.location.pathname.split("/")[2]} has no similarity results.
            </h1>);
        }

        /*
        For each photo from get_photo_by_similarity, creates a thumbnail
         */
        const photos = this.getPhotoGrid(this.state.similarPhotosData, {"photoSize": [400, 400]});

        return (<>
            <div className="page row">
            </div>
            <div className="page row">
                <div className="col-12">
                    <img className="img img-fluid" src={this.state.originalPhotoData.photo_url} />
                </div>
                <div className="display-box analysis-page">
                    {photos}
                </div>
            </div>
            <Footer/>
        </>);
    }
}

SimilarityView.propTypes = {
    photoNumber: PropTypes.number,
    mapSquareNumber: PropTypes.number,
    numSimilarPhotos: PropTypes.number
};
