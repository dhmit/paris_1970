import React from 'react';
import * as PropTypes from 'prop-types';

import Navbar from '../about/navbar';
import { Footer } from '../UILibrary/components';

export class SimilarityView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photoData: null,
        };
    }

    async componentDidMount() {
        try {
            const apiURL = `/api/photo/${this.props.mapSquareNumber}/${this.props.photoNumber}/`;
            const response = await fetch(apiURL);
            if (!response.ok) {
                this.setState({ loading: false });
            } else {
                const photoData = await response.json();
                this.setState({ photoData, loading: false });
            }
        } catch (e) {
            console.log(e);
        }
    }

    changeSide = (displaySide) => {
        this.setState({ displaySide: displaySide });
    };

    render() {
        if (this.state.loading) {
            return (<h1>
                Loading!
            </h1>);
        }

        if (!this.state.photoData) {
            return (<h1>
                Photo with id {window.location.pathname.split('/')[2]} is not in database.
            </h1>);
        }

        const {
            alt,
            number: photoNumber,
            map_square_number: mapSquareNumber,
            photographer_name: photographerName,
            photographer_number: photographerNumber,
            photographer_caption: photographerCaption,
            analyses,
        } = this.state.photoData;

        const similarPhotosResultObj = analyses.filter(
            (analysisObject) => analysisObject.name === 'resnet18_cosine_similarity',
        )[0];
        const similarPhotos = JSON.parse(similarPhotosResultObj.result);

        return (<>
            <Navbar />
            <div className="page row">
                <div className='image-info col-12 col-lg-6'>
                    {similarPhotos.map((photo, k) => (
                        <a
                            key={k}
                            href={`/photo/${photo['map_square_number']}/${photo['number']}/`}
                        >
                            <img
                                alt={photo.alt}
                                height={100}
                                width={100}
                                src={this.getSource(photo)}
                            />
                        </a>
                    ))}
                </div>
            </div>
            <Footer />
        </>);
    }
}
SimilarityView.propTypes = {
    photoNumber: PropTypes.number,
    mapSquareNumber: PropTypes.number,
};
