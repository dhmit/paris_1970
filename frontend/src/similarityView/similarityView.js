import React from 'react';
import * as PropTypes from 'prop-types';

import Navbar from '../about/navbar';
import { Footer } from '../UILibrary/components';

const SIDES = {
    CLEANED: 'cleaned',
    FRONT: 'front',
    BACK: 'back',
    BINDER: 'binder',
};


function formatPercentageValue(value) {
    return `${parseInt(value)}%`;
}

const ANALYSIS_CONFIGS = {
    whitespace_percentage: {
        formatter: formatPercentageValue,
        displayName: '% whitespace',
    },
    photographer_caption_length: {
        displayName: 'Length of photographer caption',
    },
    foreground_percentage: {
        formatter: formatPercentageValue,
        displayName: '% foreground',
    },
};

export class SimilarityView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photoData: null,
            displaySide: '',
            availableSides: [],
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
                const availableSides = Object.values(SIDES)
                    .filter((side) => photoData[`${side}_src`] !== null);
                const displaySide = availableSides.length > 0 ? availableSides[0] : '';
                this.setState({
                    photoData,
                    availableSides,
                    displaySide,
                    loading: false,
                });
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

        // const photos = this.state.photoData.map((photo, k) => {
        //     const currentAnalysis = photo['analyses'].filter(
        //         (analysisObject) => analysisObject.name === 'resnet18_cosine_similarity',
        //     )[0];
        //     return (
        //         <a
        //             key={k}
        //             title={currentAnalysis.result}
        //             href={`/photo/${photo['map_square_number']}/${photo['number']}/`}
        //         >
        //             <img
        //                 alt={photo.alt}
        //                 height={100}
        //                 width={100}
        //                 src={this.getSource(photo)}
        //             />
        //         </a>
        //     );
        // });

        return (<>
            <Navbar />
            <div className="page row">
                <div className='image-view col-12 col-lg-6'>
                    <img
                        className='image-photo'
                        src={this.state.photoData[`${this.state.displaySide}_src`]}
                        alt={alt}
                    />
                    <br/>
                    {this.state.availableSides.map((side, k) => (
                        <button key={k} onClick={() => this.changeSide(side)}>
                            {side[0].toUpperCase() + side.slice(1)} Side
                        </button>
                    ))}
                </div>
                <div className='image-info col-12 col-lg-6'>
                    <h5>Map Square</h5>
                    <p>{mapSquareNumber}</p>
                    <h5>Photo number</h5>
                    <p>{photoNumber}</p>
                    <h5>Photographer name</h5>
                    <p>{photographerName || 'Unknown'}</p>
                    <h5>Photographer number</h5>
                    <p>{photographerNumber || 'Unknown'}</p>
                    <h5>Photographer caption</h5>
                    <p>{photographerCaption || 'None'}</p>
                    {analyses.map((analysisResult, index) => {
                        const analysisConfig = ANALYSIS_CONFIGS[analysisResult.name];
                        const parsedValue = JSON.parse(analysisResult.result);
                        let analysisDisplayName;
                        let analysisResultStr = parsedValue;
                        if (!analysisConfig) {
                            analysisDisplayName = analysisResult.name;
                        } else {
                            analysisDisplayName = analysisConfig.displayName;
                            if (analysisConfig.formatter) {
                                analysisResultStr = analysisConfig.formatter(parsedValue);
                            }
                        }

                        return (
                            <React.Fragment key={index}>
                                <h5>{analysisDisplayName}</h5>
                                <p>{analysisResultStr}</p>
                            </React.Fragment>
                        );
                    })}
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