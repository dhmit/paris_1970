import React from 'react';
import Navbar from '../about/Navbar';
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
            photo_data: null,
            display_side: '',
            available_sides: [],
        };
    }

    async componentDidMount() {
        try {
            const photoId = window.location.pathname.split('/')[2];
            const response = await fetch(`/api/photo/${photoId}/`);
            if (!response.ok) {
                this.setState({ loading: false });
            } else {
                const photo_data = await response.json();
                const available_sides = Object.values(SIDES)
                    .filter((side) => photo_data[`${side}_src`] !== '');
                const display_side = available_sides.length > 0 ? available_sides[0] : '';
                this.setState({
                    photo_data,
                    available_sides,
                    display_side,
                    loading: false,
                });
            }
        } catch (e) {
            console.log(e);
        }
    }

    changeSide = (display_side) => {
        this.setState({ display_side });
    };

    render() {
        if (this.state.loading) {
            return (<h1>
                Loading!
            </h1>);
        }
        if (!this.state.photo_data) {
            return (<h1>
                Photo with id {window.location.pathname.split('/')[2]} is not in database.
            </h1>);
        }
        const {
            alt,
            map_square_number: mapSquareNumber,
            photographer_name: photographerName,
            photographer_number: photographerNumber,
            analyses,
        } = this.state.photo_data;

        console.log(analyses);

        return (<>
            <Navbar />
            <div className="page row">
                <div className='image-view col-12 col-lg-6'>
                    <img
                        className='image-photo'
                        src={this.state.photo_data[`${this.state.display_side}_src`]}
                        alt={alt}
                    />
                    <br/>
                    {this.state.available_sides.map((side, k) => {
                        if (side !== this.state.display_side) {
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
                    <h5>Photographer name</h5>
                    <p>{photographerName || 'Unknown'}</p>
                    <h5>Photographer number</h5>
                    <p>{photographerNumber || 'Unknown'}</p>
                    <h5>Map Square</h5>
                    <p>{mapSquareNumber}</p>
                    {analyses.map((analysisResult, index) => {
                        const analysisConfig = ANALYSIS_CONFIGS[analysisResult.name];
                        const analysisDisplayName = analysisConfig.displayName;
                        let analysisResultStr;
                        if (analysisConfig.formatter) {
                            analysisResultStr = analysisConfig.formatter(analysisResult.result);
                        } else {
                            analysisResultStr = analysisConfig.result.toString();
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
