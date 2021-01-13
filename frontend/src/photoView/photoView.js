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

export class FindVanishingPointDisplayWidget extends React.Component {
    render() {
        const items = [];
        let line;
        for (line of this.props.lineCoords) {
            line['1_y'] = (line['1_y'] * this.props.height) / this.props.natHeight;
            line['2_y'] = (line['2_y'] * this.props.height) / this.props.natHeight;
            line['1_x'] = (line['1_x'] * this.props.width) / this.props.natWidth;
            line['2_x'] = (line['2_x'] * this.props.width) / this.props.natWidth;
            items.push(<line
                x1={line['1_x']}
                y1={line['1_y']}
                x2={line['2_x']}
                y2={line['2_y']}
            />);
        }
        if (this.props.vanishingPointCoord !== null) {
            items.push(<circle
                cx={(this.props.vanishingPointCoord.x * this.props.width) / this.props.natWidth}
                cy={(this.props.vanishingPointCoord.y * this.props.height) / this.props.natHeight}
                r='10'
            />);
        }
        return (
            <div>
                <svg
                    className='analysis-overlay positionTopLeft'
                    height={this.props.height}
                    width={this.props.width}
                >
                    {items}
                </svg>
            </div>
        );
    }
}

function configAnalysisFindVanishingPoint(parsedValue, height, width, natHeight, natWidth) {
    const {
        line_coords: lineCoords,
        vanishing_point_coord: vanishingPointCoord,
    } = parsedValue;
    return (
        <FindVanishingPointDisplayWidget
            vanishingPointCoord={vanishingPointCoord}
            lineCoords={lineCoords}
            height={height}
            width={width}
            natHeight={natHeight}
            natWidth={natWidth}
        />
    );
}

FindVanishingPointDisplayWidget.propTypes = {
    vanishingPointCoord: PropTypes.object,
    lineCoords: PropTypes.array,
    height: PropTypes.number,
    width: PropTypes.number,
    natHeight: PropTypes.number,
    natWidth: PropTypes.number,
};

export class ForegroundPercentageDisplayWidget extends React.Component {
    render() {
        const items = [];
        const ratio = this.props.width / this.props.natWidth;
        for (const pixel of this.props.blackPixels) {
            items.push(<rect
                y={pixel[0] * ratio}
                x={pixel[1] * ratio}
                width={20 * ratio}
                height={20 * ratio}
            />);
        }
        return (
            <div>
                <svg
                    className='analysis-overlay positionTopLeft'
                    height={this.props.height}
                    width={this.props.width}
                >
                    {items}
                </svg>
            </div>
        );
    }
}

function configAnalysisForegroundPercentage(parsedValue, height, width, natHeight, natWidth) {
    const {
        percent,
        mask: blackPixels,
    } = parsedValue;
    return (
        <ForegroundPercentageDisplayWidget
            percent={percent}
            blackPixels={blackPixels}
            height={height}
            width={width}
            natHeight={natHeight}
            natWidth={natWidth}
        />
    );
}

ForegroundPercentageDisplayWidget.propTypes = {
    percent: PropTypes.number,
    blackPixels: PropTypes.array,
    height: PropTypes.number,
    width: PropTypes.number,
    natHeight: PropTypes.number,
    natWidth: PropTypes.number,
};

export class YoloModelDisplayWidget extends React.Component {
    render() {
        const items = [];
        let box;
        const ratio = this.props.height / this.props.natHeight;
        for (box of this.props.boxes) {
            items.push(
                <rect
                    className = 'outsideBox'
                    x = {box['x_coord'] * ratio}
                    y = {box['y_coord'] * ratio}
                    height = {box['height'] * ratio}
                    width = {box['width'] * ratio}
                />,
                <g className={'boxGroup'}>
                    <text
                        className='label'
                        x = {box['x_coord'] * ratio}
                        y = {box['y_coord'] * ratio - 5}
                    >
                        {box['label']}
                    </text>
                    <rect
                        className = 'boundingBox'
                        x = {box['x_coord'] * ratio}
                        y = {box['y_coord'] * ratio}
                        height = {box['height'] * ratio}
                        width = {box['width'] * ratio}
                    />
                </g>,
            );
        }

        return (
            <div>
                <svg
                    className='analysis-overlay positionTopLeft'
                    height={this.props.height}
                    width={this.props.width}
                >
                    {items}
                </svg>
            </div>
        );
    }
}

function configAnalysisYoloModel(parsedValue, height, width, natHeight, natWidth) {
    let boxes = [];
    if ('boxes' in parsedValue) {
        boxes = parsedValue['boxes'];
    }
    return (
        <YoloModelDisplayWidget
            boxes={boxes}
            height={height}
            width={width}
            natHeight={natHeight}
            natWidth={natWidth}
        />
    );
}

YoloModelDisplayWidget.propTypes = {
    boxes: PropTypes.array,
    height: PropTypes.number,
    width: PropTypes.number,
    natHeight: PropTypes.number,
    natWidth: PropTypes.number,
};

const VISUAL_ANALYSES = {
    'find_vanishing_point': [configAnalysisFindVanishingPoint, 1],
    'foreground_percentage': [configAnalysisForegroundPercentage, 2],
    'yolo_model': [configAnalysisYoloModel, 3],
};

const photoArray = [];

function formatPercentageValue(value) {
    return `${parseInt(value)}%`;
}

function formatCoordinate(value) {
    return `(${parseInt(value[0][0])}, ${parseInt(value[0][1])})`;
}

const formatBoolean = (value) => {
    return value ? 'Yes' : 'No';
};

const ANALYSIS_CONFIGS = {
    'whitespace_percentage': {
        formatter: formatPercentageValue,
        displayName: '% whitespace',
    },
    'photographer_caption_length': {
        displayName: 'Length of photographer caption',
    },
    'foreground_percentage': {
        formatter: formatPercentageValue,
        displayName: '% foreground',
    },
    'find_vanishing_point': {
        formatter: formatCoordinate,
        displayName: 'Vanishing Point Coordinate',
    },
    'portrait_detection': {
        formatter: formatBoolean,
        displayName: 'Is It a Portrait',
    },
    'indoor_analysis.combined_indoor': {
        formatter: formatBoolean,
        displayName: 'Is It Taken Indoors?',
    },
    'text_ocr': {
        displayName: 'Text Detected',
    },
    'mean_detail': {
        // formatter: formatPercentageValue,
        displayName: 'Average Amount of Detail',
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
            width: null,
            height: null,
            natWidth: null,
            natHeight: null,
            labels: null,
            mapData: null,
            prevLink: null,
            nextLink: null,
        };
        this.onImgLoad = this.onImgLoad.bind(this);
        this.photoRef = React.createRef();
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
        try {
            const mapResponse = await fetch('/api/all_map_squares/');
            const mapData = await mapResponse.json();
            this.setState({
                mapData,
                loading: false,
            });
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
        this.setState({
            width: img.clientWidth,
            height: img.clientHeight,
            natWidth: img.naturalWidth,
            natHeight: img.naturalHeight,
        });
    }

    handleResize() {
        const img = this.photoRef.current;
        this.setState({
            height: img.getBoundingClientRect()['height'],
            width: img.getBoundingClientRect()['width'],
        });
    }

    setLinks = (prevLink, nextLink) => {
        this.setState({
            prevLink: prevLink,
            nextLink: nextLink,
        });
    }

    render() {
        if (this.state.loading || !this.state.mapData) {
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

        // Resize SVG overlays on viewport resize
        window.addEventListener('resize', () => this.handleResize());

        if (photoArray.length === 0) {
            for (const mapSquare of this.state.mapData) {
                for (const photoData of mapSquare.photos) {
                    let url = window.location.origin;
                    url += `/photo/${photoData.map_square_number}/${photoData.number}/`;
                    photoArray.push(url);
                }
            }
            const idx = photoArray.indexOf(window.location.href);
            const prevLink = photoArray[(idx - 1) % photoArray.length];
            const nextLink = photoArray[(idx + 1) % photoArray.length];
            this.setLinks(prevLink, nextLink);
        }

        return (<>
            <Navbar />
            <div className= 'top-button row'>
                <div className='center'>
                    <a href={this.state.prevLink} className="navButton mx-4">&#8249;</a>
                    <a href={this.state.nextLink} className="navButton mx-4">&#8250;</a>
                </div>
            </div>
            <div className="page row">
                <div className='image-view col-12 col-lg-6'>
                    <div>
                        <img
                            className='image-photo positionTopLeft'
                            src={this.state.photoData[`${this.state.displaySide}_src`]}
                            alt={alt}
                            onLoad={this.onImgLoad}
                            ref={this.photoRef}
                        />

                        {analyses.map((analysisResult) => {
                            const parsedValue = JSON.parse(analysisResult.result);

                            if (analysisResult.name in VISUAL_ANALYSES
                                && this.state.displaySide === 'cleaned') {
                                if (VISUAL_ANALYSES[analysisResult.name][1] === this.state.view) {
                                    return VISUAL_ANALYSES[analysisResult.name][0](
                                        parsedValue,
                                        this.state.height,
                                        this.state.width,
                                        this.state.natHeight,
                                        this.state.natWidth,
                                    );
                                }
                                return null;
                            }
                            // handled in a different div
                            return null;
                        })}
                        <svg
                            height={this.state.height}
                            width={this.state.width}
                        >
                        </svg>
                    </div>
                    <br/>
                    <div className={'centerBtn'}>
                        {this.state.availableSides.map((side, k) => (
                            <button
                                className='btn btn-outline-dark mx-1'
                                key={k}
                                onClick={() => this.changeSide(side)}
                            >
                                {side[0].toUpperCase() + side.slice(1)} Side
                            </button>
                        ))}
                    </div>
                </div>
                <div className='image-info col-12 col-lg-6'>
                    <h5>Map Square</h5>
                    <p>{mapSquareNumber}</p>
                    <h5>Photo Number</h5>
                    <p>{photoNumber}</p>
                    <h5>Photographer Name</h5>
                    <p>{photographerName || 'Unknown'}</p>
                    <h5>Photographer number</h5>
                    <p>
                        {
                            photographerNumber
                                ? <a href={`/photographer/${photographerNumber}/`}>
                                    {photographerNumber}
                                </a>
                                : 'Unknown'
                        }
                    </p>
                    <h5>Photographer caption</h5>
                    <p>{photographerCaption || 'None'}</p>

                    <h5>Visual Analysis</h5>
                    <div className="row">
                        <div className="col-6">
                            {(this.state.displaySide === 'cleaned')
                                ? <select
                                    id="toggleSelect"
                                    className="custom-select"
                                    onChange={this.toggleStatus}
                                    value={this.state.view}
                                >
                                    <option value="0">None selected</option>
                                    <option value="1">Perspective Lines</option>
                                    <option value="2">Foreground Mask</option>
                                    <option value="3">YOLO Model</option>
                                </select>
                                : <p>Not available</p>
                            }
                            {(this.state.view === 3 && this.state.displaySide === 'cleaned')
                                ? <p className={'px-3 my-0'}>
                                    <i>Hover over the boxes to see the name of the object.</i>
                                </p>
                                : <span></span>
                            }
                        </div>
                    </div>

                    {analyses.map((analysisResult, index) => {
                        const analysisConfig = ANALYSIS_CONFIGS[analysisResult.name];
                        const parsedValue = JSON.parse(analysisResult.result);

                        if (analysisResult.name === 'yolo_model') {
                            let labels = [];
                            if ('labels' in parsedValue) {
                                labels = parsedValue['labels'];
                            } else {
                                return (
                                    <React.Fragment>
                                        <h5>Objects Detected</h5>
                                        <p>None</p>
                                    </React.Fragment>
                                );
                            }
                            return (
                                <React.Fragment>
                                    <h5>Objects Detected</h5>
                                    <ul>
                                        {Object.keys(labels).map((key, i) => (
                                            <li key={i}>{key}: {labels[key]}</li>
                                        ))}
                                    </ul>
                                </React.Fragment>
                            );
                        }

                        if (analysisResult.name === 'photo_similarity.resnet18_cosine_similarity') {
                            if (parsedValue === []) {
                                return (
                                    <React.Fragment>
                                        <h5>Similar Photos</h5>
                                        <p>None</p>
                                    </React.Fragment>
                                );
                            }
                            return (
                               <React.Fragment>
                                  <h5>Similar Photos</h5>
                                  <ul>
                                      {parsedValue.map((photo, i) => (
                                          <li key={i}>Map Square {photo[0]}, Photo {photo[1]}, Similarity: {photo[2] * 100}%</li>
                                      ))}
                                  </ul>
                               </React.Fragment>
                            );
                        }

                        // handled in a different div
                        if (analysisResult.name in VISUAL_ANALYSES) {
                            return null;
                        }

                        let analysisDisplayName;
                        let analysisResultStr = analysisResult.result;
                        if (!analysisConfig) {
                            analysisDisplayName = analysisResult.name;
                        } else {
                            analysisDisplayName = analysisConfig.displayName;
                            if (analysisConfig.formatter) {
                                analysisResultStr = analysisConfig.formatter(analysisResult.result);
                            }
                        }
                        if (['null', '""'].includes(analysisResultStr)) {
                            analysisResultStr = 'N/A';
                        }

                        return (
                            <React.Fragment key={index}>
                                <h5>{analysisDisplayName}</h5>
                                <p>{analysisResultStr}</p>
                            </React.Fragment>
                        );
                    })}


                </div>
                <div className='center'>
                    <a href={this.state.prevLink} className="navButton mx-4">&#8249;</a>
                    <a href={this.state.nextLink} className="navButton mx-4">&#8250;</a>
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
