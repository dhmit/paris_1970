import React from 'react';
import * as PropTypes from 'prop-types';

import Navbar from '../about/navbar';
import { Footer } from '../UILibrary/components';


const ANALYSIS = {
    whitespace_percentage: {
        displayName: 'Average Whitespace Percentage',
        accumulateFn: (old, value) => old + parseFloat(value),
    },
    portrait_detection: {
        displayName: 'Percentage of Portraits',
        accumulateFn: (old, value) => old + (value === 'true' ? 1 : 0),
    },
};

export class PhotographerView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photographerData: null,
        };
    }

    async componentDidMount() {
        try {
            const response = await fetch(`/api/photographer/${this.props.photographerNumber}/`);
            if (!response.ok) {
                this.setState({ loading: false });
            } else {
                const photographerData = await response.json();
                this.setState({
                    photographerData,
                    loading: false,
                });
            }
        } catch (e) {
            console.log(e);
        }
    }

    getAggregatePhotoAnalysis = (photos) => {
        const analysisAcc = {};
        Object.keys(ANALYSIS).forEach((analysisName) => {
            analysisAcc[analysisName] = 0;
        });
        photos.forEach((photo) => {
            photo['analyses'].forEach((analysis) => {
                const analysisName = analysis.name;
                const result = analysis.result;
                console.log(result);
                analysisAcc[analysisName] = ANALYSIS[analysisName].accumulateFn(
                    analysisAcc[analysisName],
                    result,
                );
                console.log(analysisAcc);
            });
        });

        const results = {};
        Object.keys(analysisAcc).forEach((analysisName) => {
            results[analysisName] = analysisAcc[analysisName] / photos.length;
        });
        return results;
    };

    render() {
        if (this.state.loading) {
            return (<>
                Loading!
            </>);
        }
        if (!this.state.photographerData) {
            return (<>
                Photographer number ${this.props.photographerNumber} is not in the database.
            </>);
        }
        const {
            name,
            map_square: mapSquare,  // n.b. here we rename while doing the object destructuring
            number,
            sentiment,
            type,
            photos,
        } = this.state.photographerData;

        const photographerAnalysis = this.getAggregatePhotoAnalysis(photos);
        return (<>
            <Navbar/>
            <div className='page'>
                <h1>{name} (ID: {number})</h1>
                <h2 className="h3">Assigned to:</h2>
                <h3 className="h5">Map Square {mapSquare.number}</h3>
                <h2 className="h3">Analysis Results</h2>
                {Object.keys(photographerAnalysis).map((analysis) => {
                    return (
                        <div key={analysis}>
                            <h3 className="h5">{ANALYSIS[analysis].displayName}:</h3>
                            {photographerAnalysis[analysis]}
                        </div>
                    );
                })}
                <h2 className="h3">Photos:</h2>
                <div className='photo_gallery'>
                    {photos.map((photo, k) => (
                        <div className="photo" key={k}>
                            <a
                                key={k}
                                href={`/photo/${photo['map_square_number']}/${photo['number']}/`}
                            >
                                <img
                                    alt={photo.alt}
                                    height={200}
                                    width={200}
                                    src={photo['thumbnail_src']}
                                />
                            </a>
                        </div>
                    ))}
                </div>
            </div>
            <Footer/>
        </>);
    }
}
PhotographerView.propTypes = {
    photographerNumber: PropTypes.number,
};
