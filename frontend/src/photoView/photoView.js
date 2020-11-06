import React from 'react';
import * as PropTypes from 'prop-types';

import Navbar from '../about/navbar';
import { Footer } from '../UILibrary/components';

export class CoordDisplayWidget extends React.Component {
    render() {
        const items = [];
        let line;
        for (line of this.props.lineCoords) {
            line['1_y'] = (line['1_y'] * this.props.height) / this.props.naturalHeight;
            line['2_y'] = (line['2_y'] * this.props.height) / this.props.naturalHeight;
            line['1_x'] = (line['1_x'] * this.props.width) / this.props.naturalWidth;
            line['2_x'] = (line['2_x'] * this.props.width) / this.props.naturalWidth;
            items.push(<line
                x1={line['1_x']}
                y1={line['1_y']}
                x2={line['2_x']}
                y2={line['2_y']}
            />);
        }
        if (this.props.vanishingPointCoord !== null) {
            items.push(<circle
                cx={(this.props.vanishingPointCoord.x * this.props.width) / this.props.naturalWidth}
                cy={(this.props.vanishingPointCoord.y * this.props.height) / this.props.naturalHeight}
                r='10'
            />);
        }
        return (
            <div>
                <svg
                    className='analysis-overlay floatTL'
                    height={this.props.height}
                    width={this.props.width}
                >
                    {items}
                </svg>
            </div>
        );
    }
}
CoordDisplayWidget.propTypes = {
    vanishingPointCoord: PropTypes.object,
    lineCoords: PropTypes.object,
    height: PropTypes.number,
    width: PropTypes.number,
    naturalHeight: PropTypes.number,
    naturalWidth: PropTypes.number,
};


const SIDES = {
    CLEANED: 'cleaned',
    FRONT: 'front',
    BACK: 'back',
    BINDER: 'binder',
};

function configAnalysisFV(parsedValue, height, width, naturalHeight, naturalWidth) {
    const {
        line_coords: lineCoords,
        vanishing_point_coord: vanishingPointCoord,
    } = parsedValue;
    return (
        <CoordDisplayWidget
            vanishingPointCoord={vanishingPointCoord}
            lineCoords={lineCoords}
            height={height}
            width={width}
            naturalHeight={naturalHeight}
            naturalWidth={naturalWidth}
        />
    );
}

function configAnalysisFP(parsedValue, height, width) {
    console.log(parsedValue);
    console.log(height);
    console.log(width);
    return null;
}

const VISUALANALYSISDICT = {
    'find_vanishing_point': [configAnalysisFV, 1],
    'foreground_percentage': [configAnalysisFP, 2],
};


function formatPercentageValue(value) {
    return `${parseInt(value)}%`;
}

function formatCoordinate(value) {
    return `(${parseInt(value[0][0])}, ${parseInt(value[0][1])})`;
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
    find_vanishing_point: {
        formatter: formatCoordinate,
        displayName: 'Vanishing Point Coordinate',
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
            view: 0,
            width: 1,
            height: 1,
            naturalWidth: 1,
            naturalHeight: 1,
        };
        this.onImgLoad = this.onImgLoad.bind(this);
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

    toggleStatus = (event) => {
        this.setState({
            view: parseInt(event.target.value),
        });
    }

    onImgLoad({ target: img }) {
        console.log('IMAGE LOADED');
        this.setState({
            width: img.clientWidth,
            height: img.clientHeight,
            naturalWidth: img.naturalWidth,
            naturalHeight: img.naturalHeight,
        });
    }

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

        return (<>
            <Navbar />
            <div className="page row">
                <div className='image-view col-12 col-lg-6'>
                    <div>
                        <img
                            className='image-photo floatTL'
                            src={this.state.photoData[`${this.state.displaySide}_src`]}
                            alt={alt}
                            onLoad={this.onImgLoad}
                        />

                        {analyses.map((analysisResult) => {
                            const parsedValue = JSON.parse(analysisResult.result);

                            if (analysisResult.name in VISUALANALYSISDICT) {
                                if (VISUALANALYSISDICT[analysisResult.name][1] === this.state.view) {
                                    return VISUALANALYSISDICT[analysisResult.name][0](
                                        parsedValue,
                                        this.state.height,
                                        this.state.width,
                                        this.state.naturalHeight,
                                        this.state.naturalWidth,
                                    );
                                }
                                return null;
                            }
                            // handled in a different div
                            return null;
                        })}
                    </div>
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
                    <div className="row">
                        <div className="col-6">
                            <select
                                id="toggleSelect"
                                className="custom-select"
                                onChange={this.toggleStatus}
                                value={this.state.view}
                            >
                                <option value="0">Select...</option>
                                <option value="1">Perspective Lines</option>
                                <option value="2">Foreground Mask</option>
                            </select>
                        </div>
                    </div>
                    <p>
                        {(() => {
                            switch (this.state.view) {
                            case 0: return 'Nothing selected';
                            case 1: return 'Perspective selected';
                            case 2: return 'Foreground selected';
                            default: return 'Nothing selected';
                            }
                        })()}
                        <br/>
                    </p>

                    {analyses.map((analysisResult, index) => {
                        const analysisConfig = ANALYSIS_CONFIGS[analysisResult.name];
                        const parsedValue = JSON.parse(analysisResult.result);

                        // handled in a different div
                        if (analysisResult.name in VISUALANALYSISDICT) {
                            return null;
                        }

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
PhotoView.propTypes = {
    photoNumber: PropTypes.number,
    mapSquareNumber: PropTypes.number,
};
