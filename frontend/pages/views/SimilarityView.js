import React from "react";
import * as PropTypes from "prop-types";

import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";
import LoadingPage from "../LoadingPage";

import {getSource} from "./AnalysisView";

/*
Creates a view to show the most similar photos for a photo given url with a number of photos
 */
export class SimilarityView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photoData: null
        };
    }

    async componentDidMount() {
        try {
            const apiURL = "/api/similar_photos/" +
                `${this.props.mapSquareNumber}/${this.props.photoNumber}/` +
                `${this.props.numSimilarPhotos}/`;
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

        if (this.state.photoData.length === 0) {
            return (<h1>
                Photo with id {window.location.pathname.split("/")[2]} has no similarity results.
            </h1>);
        }

        /*
        For each photo from get_photo_by_similarity, creates a thumbnail
         */
        const photos = this.state.photoData.map((photo, k) => {
            return (
                <a
                    key={k}
                    href={`/photo/${photo["map_square_number"]}/${photo["number"]}/`}>
                    <img
                        alt={photo.alt}
                        height={200}
                        width={200}
                        src={getSource(photo)}
                    />
                </a>
            );
        });

        return (<>
            <Navbar/>
            <div className="page row">
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
