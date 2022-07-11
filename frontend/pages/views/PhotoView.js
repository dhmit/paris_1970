import React from "react";
import * as PropTypes from "prop-types";

import Footer from "../../components/Footer";
import PhotoViewer from "../../components/PhotoViewer";
import LoadingPage from "../LoadingPage";

import {Dropdown} from "react-bootstrap";

let tagList = ["Construction", "People", "Building"];

export class FindVanishingPointDisplayWidget extends React.Component {
    render() {
        const items = [];
        let line;
        for (line of this.props.lineCoords) {
            line["1_y"] = (line["1_y"] * this.props.height) / this.props.natHeight;
            line["2_y"] = (line["2_y"] * this.props.height) / this.props.natHeight;
            line["1_x"] = (line["1_x"] * this.props.width) / this.props.natWidth;
            line["2_x"] = (line["2_x"] * this.props.width) / this.props.natWidth;
            items.push(<line
                x1={line["1_x"]}
                y1={line["1_y"]}
                x2={line["2_x"]}
                y2={line["2_y"]}
            />);
        }
        if (this.props.vanishingPointCoord !== null) {
            items.push(<circle
                cx={(this.props.vanishingPointCoord.x * this.props.width) / this.props.natWidth}
                cy={(this.props.vanishingPointCoord.y * this.props.height) / this.props.natHeight}
                r="10"
            />);
        }
        return (
            <div>
                <svg
                    className="analysis-overlay"
                    height={this.props.height}
                    width={this.props.width}>
                    {items}
                </svg>
            </div>
        );
    }
}

function configAnalysisFindVanishingPoint(parsedValue, height, width, natHeight, natWidth) {
    const {
        line_coords: lineCoords,
        vanishing_point_coord: vanishingPointCoord
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
    natWidth: PropTypes.number
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
                    className="analysis-overlay"
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
        mask: blackPixels
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
    natWidth: PropTypes.number
};

export class YoloModelDisplayWidget extends React.Component {
    render() {
        const items = [];
        let box;
        const ratio = this.props.height / this.props.natHeight;
        for (box of this.props.boxes) {
            items.push(
                <rect
                    className="outsideBox"
                    x={box["x_coord"] * ratio}
                    y={box["y_coord"] * ratio}
                    height={box["height"] * ratio}
                    width={box["width"] * ratio}
                />,
                <g className={"boxGroup"}>
                    <text
                        className="label"
                        x={box["x_coord"] * ratio}
                        y={box["y_coord"] * ratio - 5}
                    >
                        {box["label"]}
                    </text>
                    <rect
                        className="boundingBox"
                        x={box["x_coord"] * ratio}
                        y={box["y_coord"] * ratio}
                        height={box["height"] * ratio}
                        width={box["width"] * ratio}
                    />
                </g>
            );
        }

        return (
            <div>
                <svg
                    className="analysis-overlay"
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
    if ("boxes" in parsedValue) {
        boxes = parsedValue["boxes"];
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
    natWidth: PropTypes.number
};

const VISUAL_ANALYSES = {
    "find_vanishing_point": [configAnalysisFindVanishingPoint, 1],
    "foreground_percentage": [configAnalysisForegroundPercentage, 2],
    "yolo_model": [configAnalysisYoloModel, 3]
};

function formatPercentageValue(value) {
    return `${parseInt(value)}%`;
}

export class PhotoView extends PhotoViewer {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photoData: null,
            displaySide: "photo",
            availableSides: [],
            view: 0,
            width: null,
            height: null,
            natWidth: null,
            natHeight: null,
            labels: null,
            mapData: null,
            prevLink: null,
            nextLink: null
        };
        this.onImgLoad = this.onImgLoad.bind(this);
        this.photoRef = React.createRef();
    }

    async componentDidMount() {
        const mapPhotoString = `${this.props.mapSquareNumber}/${this.props.photoNumber}/`;
        try {
            const apiURL = "/api/photo/" + mapPhotoString;
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
        try {
            const photoResponse = await fetch("/api/prev_next_photos/" + mapPhotoString);
            let prevNextPhotos = await photoResponse.json();
            prevNextPhotos = prevNextPhotos.map((photo) => {
                return photo ? `/photo/${photo.map_square_number}/${photo.number}/` : null;
            });
            this.setState({
                prevLink: prevNextPhotos[0],
                nextLink: prevNextPhotos[1],
                loading: false
            });
        } catch (e) {
            console.log(e);
        }
    }

    changeSide = (displaySide) => {
        this.setState({displaySide: displaySide});
    };

    toggleStatus = (event) => {
        this.setState({
            view: parseInt(event.target.value)
        });
    };

    onImgLoad({target: img}) {
        this.setState({
            width: img.clientWidth,
            height: img.clientHeight,
            natWidth: img.naturalWidth,
            natHeight: img.naturalHeight
        });
    }

    handleResize() {
        const img = this.photoRef.current;
        this.setState({
            height: img.getBoundingClientRect()["height"],
            width: img.getBoundingClientRect()["width"]
        });
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
        const {
            alt,
            number: photoNumber,
            map_square_number: mapSquareNumber,
            photographer_name: photographerName,
            photographer_number: photographerNumber,
            photographer_caption: photographerCaption,
            analyses
        } = this.state.photoData;

        // Resize SVG overlays on viewport resize
        window.addEventListener("resize", () => this.handleResize());

        const visualAnalyses = [];
        for (const [analysisName, result] of Object.entries(analyses)) {
            let visualAnalysis = null;
            if (analysisName in VISUAL_ANALYSES && this.state.displaySide === "photo") {
                if (VISUAL_ANALYSES[analysisName][1] !== this.state.view) continue;
                visualAnalysis = VISUAL_ANALYSES[analysisName][0](
                    result,
                    this.state.height,
                    this.state.width,
                    this.state.natHeight,
                    this.state.natWidth
                );
            }
            // handled in a different div
            visualAnalyses.push(visualAnalysis);
        }

        const yoloResult = (
            "yolo_model" in analyses
                ? analyses["yolo_model"]
                : {}
        );

        const similarPhotos = (
            "photo_similarity.resnet18_cosine_similarity" in analyses
                ? analyses["photo_similarity.resnet18_cosine_similarity"]
                : []
        );

        return (<>
            <div className="page">
                <div className="d-flex justify-content-center">
                    <a href={this.state.prevLink} className="navButton mx-4">&#8249;</a>
                    <a href={this.state.nextLink} className="navButton mx-4">&#8250;</a>
                </div>
                <br/>
                <div className="page row">
                    <div className="image-view col-12 col-lg-6">
                        <div className="image-box">
                            <img
                                className="image-photo position-top-left"
                                src={this.getSource(this.state.photoData, this.state.displaySide)}
                                alt={alt}
                                onLoad={this.onImgLoad}
                                ref={this.photoRef}
                            />
                            {visualAnalyses}
                        </div>
                        <br/>
                        <div className={"centerBtn"}>
                            <button
                                className={"side-button"}
                                onClick={() => this.changeSide("photo")}>
                                PHOTO
                            </button>
                            <button
                                className={"side-button"}
                                onClick={() => this.changeSide("slide")}>
                                SLIDE
                            </button>
                        </div>
                        {/* TODO: Disable scroll buttons when no more photos to scroll through */}
                        <div className="similar-photos-box">
                            <button
                                type="button"
                                className="similarity-scroll btn btn-dark"
                                onClick={
                                () => document.getElementById("sim-photos").scrollLeft -=
                                    document.getElementById("sim-photos").clientWidth}
                            >{"<"}</button>

                            <div id="sim-photos" className="similar-photos">
                                {this.getPhotoGrid(
                                    similarPhotos,
                                    {
                                        "className": "similar-photo",
                                        "titleFunc": (k, photo) =>
                                        `Map Square: ${photo["map_square_number"]}, ` +
                                        `Photo: ${photo["number"]}, Similarity: ${photo["similarity"]}`
                                    }
                                )}
                            </div>

                            <button
                                type="button"
                                className="similarity-scroll btn btn-dark"
                                onClick={
                                () => document.getElementById("sim-photos").scrollLeft +=
                                    document.getElementById("sim-photos").clientWidth}
                            >{">"}</button>
                        </div>
                    </div>
                    <div className="image-info col-12 col-lg-6">
                        <h4>Photograph Details</h4>
                        <br></br>
                        <h6>PHOTOGRAPHER</h6>
                        <p>
                            {photographerName || "Unknown"}
                            {
                                photographerNumber
                                    ? <span>
                                        {" (Number: "}
                                        <a href={`/photographer/${photographerNumber}/`}>
                                            {photographerNumber}
                                        </a>
                                    )
                                    </span>
                                    : " (Number: Unknown)"
                            }
                        </p>
                        <br></br>
                        <h6>TAGS</h6>

                        {tagList.map((word) => (
                            <button className="tag-button" key={word.id}>
                                {word}
                            </button>
                        ))}

                        <br></br><br></br>
                        <h6>CAPTION</h6>
                        <p>{photographerCaption || "None"}</p>
                        <br></br>

                        <h6>LOCATION</h6>
                        <p>Map Square:
                            <a href={`/map_square/${mapSquareNumber}`}>{mapSquareNumber}</a>
                        </p>
                        <p>Photo: {photoNumber}</p>

                        <h6>ANALYSIS</h6>

                        <Dropdown className="photo-sort-dropdown">
                            <Dropdown.Toggle className="photo-sort-dropdown-button" align="start">
                                Sort By...
                            </Dropdown.Toggle>

                            <Dropdown.Menu>
                                <Dropdown.Item href="#/action-1">Action</Dropdown.Item>
                                <Dropdown.Item href="#/action-2">Another action</Dropdown.Item>
                                <Dropdown.Item href="#/action-3">Something else</Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>

                        <div className="row">
                            <div className="col-6">
                                {(this.state.displaySide === "photo")
                                    ? <select
                                        id="toggleSelect"
                                        className="custom-select"
                                        onChange={this.toggleStatus}
                                        value={this.state.view}>
                                        <option value="0">None selected</option>
                                        <option value="1">Perspective Lines</option>
                                        <option value="2">Foreground Mask</option>
                                        <option value="3">YOLO Model</option>
                                    </select>
                                    : <p>Not available</p>
                                }
                                {(this.state.view === 3 && this.state.displaySide === "photo")
                                    ? <p className={"px-3 my-0"}>
                                        <i>Hover over the boxes to see the name of the object.</i>
                                    </p>
                                    : <></>
                                }
                            </div>
                        </div>

                        {"labels" in yoloResult
                            ? <React.Fragment>
                                <h5>Objects Detected</h5>
                                <ul>
                                    {Object.keys(yoloResult["labels"])
                                    .map((key, i) => (
                                        <li key={i}>
                                            {key}: {yoloResult["labels"][key]}
                                        </li>
                                    ))}
                                </ul>
                            </React.Fragment>
                            : <React.Fragment>
                                <h5>Objects Detected</h5>
                                <p>None</p>
                            </React.Fragment>
                        }

                        {!(similarPhotos in [[], null])
                            ? <React.Fragment>
                                <h5>Similar Photos (% Similarity)</h5>
                                <h6>
                                    <a href={"/similar_photos/" +
                                    `${this.props.mapSquareNumber}/` +
                                    `${this.props.photoNumber}/10/`}>
                                        View Top 10 Similar Photos
                                    </a>
                                </h6>
                                <div
                                    className="col pb-scroll"
                                    id="scrolling"
                                    style={{
                                        maxHeight: 200,
                                        overflow: "auto"
                                    }}>
                                    {similarPhotos.map((photo, i) => (
                                        <div key={i}>
                                            <a href={`/photo/${photo["map_square_number"]}/${photo["number"]}/`}>
                                                Map Square {photo["map_square_number"]},
                                                Photo {photo["number"]}
                                            </a>
                                            ({formatPercentageValue(photo["similarity"] * 100)})
                                        </div>
                                    ))}
                                </div>
                            </React.Fragment>
                            : <React.Fragment>
                                <h5>Similar Photos</h5>
                                <p>None</p>
                            </React.Fragment>
                        }
                    </div>
                </div>
            </div>
            <Footer/>
        </>);
    }
}

PhotoView.propTypes = {
    photoNumber: PropTypes.number,
    mapSquareNumber: PropTypes.number,
    photo_dir: PropTypes.string
};
