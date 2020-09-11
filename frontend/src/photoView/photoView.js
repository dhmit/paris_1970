import React from 'react';
import Navbar from '../about/navbar';
import { Footer } from '../UILibrary/components';

const SIDES = {
    FRONT: 'front',
    BACK: 'back',
    BINDER: 'binder',
};

const ANALYSIS_CONFIGS = {
    whitespace_percentage: {
        formatter: (value) => `${parseInt(value)}%`,
        displayName: '% whitespace',
    },
    photographer_caption_length: {
        displayName: 'Length of photographer caption',
    },
};

export class PhotoView extends React.Component {
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
            const photoId = window.location.pathname.split('/')[2];
            const response = await fetch(`/api/photo/${photoId}/`);
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

        console.log(analyses);

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
                    {this.state.availableSides.map((side, k) => {
                        if (side !== this.state.displaySide) {
                            return (
                                <button key={k} onClick={() => this.changeSide(side)}>
                                    {side[0].toUpperCase() + side.slice(1)} Side
                                </button>
                            );
                        }
                        return '';
                    })}

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
                    <p>{photographerCaption}</p>
                    {analyses.map((analysisResult, index) => {
                        const analysisConfig = ANALYSIS_CONFIGS[analysisResult.name];
                        const analysisDisplayName = analysisConfig.displayName;
                        let analysisResultStr;
                        if (analysisConfig.formatter) {
                            analysisResultStr = analysisConfig.formatter(analysisResult.result);
                        } else {
                            analysisResultStr = analysisResult.result.toString();
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
