import React from "react";
import * as PropTypes from "prop-types";

import Footer from "../../components/Footer";
import PhotoViewer from "../../components/PhotoViewer";
import LoadingPage from "../LoadingPage";


const percentFormat = (x) => Math.floor(x) + "%";
const numberFormat = (x) => Math.floor(x);

const ANALYSIS = {
    whitespace_percentage: {
        displayName: "Average Whitespace Percentage",
        analysisType: "average",
        displayFormat: percentFormat
    },
    portrait_detection: {
        displayName: "Percentage of Portraits",
        analysisType: "count",
        displayFormat: percentFormat
    },
    mean_detail: {
        displayName: "Average Mean Detail",
        analysisType: "average",
        displayFormat: numberFormat
    },
    photographer_caption_length: {
        displayName: "Average Photographer Caption Length",
        analysisType: "none",
        displayFormat: numberFormat
    },
    yolo_model: {
        displayName: "Yolo Model",
        analysisType: "none",
        displayFormat: numberFormat
    },
    text_ocr: {
        displayName: "text_ocr",
        analysisType: "none",
        displayFormat: numberFormat
    }
};

export class PhotographerView extends PhotoViewer {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photographerData: null
        };
    }

    async componentDidMount() {
        try {
            const response = await fetch(`/api/photographer/${this.props.photographerNumber}/`);
            if (!response.ok) {
                this.setState({loading: false});
            } else {
                const photographerData = await response.json();
                this.setState({
                    photographerData,
                    loading: false
                });
            }
        } catch (e) {
            console.log(e);
        }
    }

    getAggregatePhotoAnalysis = (photos) => {
        const analysisAcc = {};
        Object.keys(ANALYSIS)
        .forEach((analysisName) => {
            analysisAcc[analysisName] = 0;
        });
        photos.forEach((photo) => {
            photo["analyses"].forEach((analysis) => {
                const analysisName = analysis.name;
                const result = analysis.result;
                const analysisType = ANALYSIS[analysisName].analysisType;
                if (analysisType === "average") {
                    analysisAcc[analysisName] += parseFloat(result);
                } else if (analysisType === "count") {
                    analysisAcc[analysisName] += 1;
                }
            });
        });

        const results = {};
        Object.keys(analysisAcc)
        .forEach((analysisName) => {
            const analysisType = ANALYSIS[analysisName].analysisType;
            let result;
            if (analysisType === "average") {
                result = analysisAcc[analysisName] / photos.length;
            } else if (analysisType === "count") {
                result = analysisAcc[analysisName];
            }
            results[analysisName] = ANALYSIS[analysisName].displayFormat(result);
        });
        return results;
    };

    render() {
        if (this.state.loading) {
            return (<LoadingPage/>);
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
            photos
        } = this.state.photographerData;

        // const photographerAnalysis = this.getAggregatePhotoAnalysis(photos);
        const photographerAnalysis = [];
        return (<>
            <div className="page row">
                <div className="col-6">
                    <h1>{name} (ID: {number})</h1>
                    <h2 className="h3">Assigned to:</h2>
                    <h3 className="h5">Map Square {mapSquare.number}</h3>
                </div>
                <div className="col-6">
                    <h2 className="h3">Analysis Results</h2>
                    {Object.keys(photographerAnalysis)
                    .map((analysis) => {
                        if (ANALYSIS[analysis].analysisType !== "none") {
                            return (
                                <div key={analysis}>
                                    <h3 className="h5">{ANALYSIS[analysis].displayName}:</h3>
                                    {photographerAnalysis[analysis]}
                                </div>
                            );
                        }
                        return "";
                    })}
                </div>
                <h2 className="h3">Photos Gallery:</h2>
                <div className="photo_gallery">
                    {this.getPhotoGrid(
                        photos, {"className": "photo", "photoSize": [150, 150]}
                    )}
                </div>
            </div>
            <Footer/>
        </>);
    }
}

PhotographerView.propTypes = {
    photographerNumber: PropTypes.number,
    photo_dir: PropTypes.string
};
