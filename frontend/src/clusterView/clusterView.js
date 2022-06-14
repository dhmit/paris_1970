import React from "react";
import * as PropTypes from "prop-types";

import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import LoadingPage from "../components/LoadingPage";
import {PhotoViewer} from "../components/PhotoViewer";


export class ClusterView extends PhotoViewer {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photoData: null
        };
    }

    async componentDidMount() {
        try {
            const apiURL = "/api/clustering/" +
                `${this.props.numberOfClusters}/${this.props.clusterNumber}/`;
            console.log(apiURL);
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

    render() {
        if (this.state.loading) {
            return (<LoadingPage/>);
        }

        console.log(this.state.photoData);
        const photos = this.getPhotoGrid(this.state.photoData);

        const prevButton = this.props.clusterNumber - 1 > 0 ? (
            <a
                title="prev"
                href={`/clustering/${this.props.numberOfClusters}/${this.props.clusterNumber - 1}/`}
            >
                <button className="order-button">
                    Prev
                </button>
            </a>) : (<></>);

        const nextButton = this.props.clusterNumber + 1 <= this.props.numberOfClusters ? (
            <a
                title="next"
                href={`/clustering/${this.props.numberOfClusters}/${this.props.clusterNumber + 1}/`}
            >
                <button className="order-button">
                    Next
                </button>
            </a>) : (<></>);

        const options = this.state.photoData.length === 0 ? (
            <p>
                {`There are no photos that are in cluster ${this.props.clusterNumber}` +
                " or the cluster number is out of bounds."}
            </p>) : (<div className="state-buttons row">{prevButton}{nextButton}</div>);

        return (<>
            <Navbar/>
            <div className="display-box cluster-page">
                <h3>
                    Number of clusters: {this.props.numberOfClusters + " "}
                    Cluster number: {this.props.clusterNumber}
                </h3>
                {options}
                <br/>
                {photos}
            </div>
            <Footer/>
        </>);
    }
}

ClusterView.propTypes = {
    numberOfClusters: PropTypes.number,
    clusterNumber: PropTypes.number
};
