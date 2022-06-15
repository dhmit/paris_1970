import React from "react";
import * as PropTypes from "prop-types";

import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";
import LoadingPage from "../LoadingPage";

const SIDES = {
    CLEANED: "cleaned",
    FRONT: "front",
    BACK: "back"
};

export const getSource = (photoData, photoDir, displaySide = false) => {
    if (!displaySide) {
        const availableSides = Object.values(SIDES)
        .filter(
            (side) => photoData[`${side}_src`]
        );
        displaySide = availableSides.length > 0 ? availableSides[0] : "";
    }
    return `${photoDir}/${photoData.map_square_number}/${photoData.number}_${displaySide}.jpg`;
};


export class AnalysisView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photoData: null,
            displayOrder: "Ascending"
        };
    }

    async componentDidMount() {
        try {
            const dictKey = this.props.objectName ? this.props.objectName : "";
            const apiURL = `/api/analysis/${this.props.analysisName}/${dictKey}`;
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

    reverseOrder = () => {
        let newOrder;
        if (this.state.displayOrder === "Descending") {
            newOrder = "Ascending";
        } else {
            newOrder = "Descending";
        }
        const newPhotoData = this.state.photoData.reverse();
        this.setState({
            photoData: newPhotoData,
            displayOrder: newOrder
        });
    };

    render() {
        if (this.state.loading) {
            return (<LoadingPage/>);
        }

        const photos = this.state.photoData.map((photo, k) => {
            const currentAnalysis = photo["analyses"].filter(
                (analysisObject) => analysisObject.name === this.props.analysisName
            )[0];
            if (photo.cleaned_src || photo.front_src) {
                return (
                    <a key={k}
                       title={currentAnalysis.result}
                       href={`/photo/${photo["map_square_number"]}/${photo["number"]}/`}>
                        <img
                            alt={photo.alt}
                            height={100}
                            width={100}
                            src={getSource(photo)}
                        />
                    </a>
                );
            }
            return "";
        });

        const options = this.state.photoData.length === 0 ? (
            <p>
                {`There are no photos that have an analysis result for ${this.props.analysisName}` +
                " or the analysis does not exist."}
            </p>) : (<div className="options">
            <p>Current photo order: {this.state.displayOrder} values</p>
            <button className="order-button" onClick={() => this.reverseOrder()}>
                Reverse photo order
            </button>
        </div>);

        const objectName = this.props.objectName ? `key: ${this.props.objectName}` : "";

        return (<>
            <Navbar/>
            <div className="display-box analysis-page">
                <h3 className="text-capitalize">{
                    this.props.analysisName.split("_")
                    .join(" ")
                }</h3>
                <h5>{objectName}</h5>
                {options}
                <br/>
                {photos}
            </div>
            <Footer/>
        </>);
    }
}

AnalysisView.propTypes = {
    analysisName: PropTypes.string,
    objectName: PropTypes.string
};
