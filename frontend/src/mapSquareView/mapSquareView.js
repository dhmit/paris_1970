import React from "react";
import * as PropTypes from "prop-types";

import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import LoadingPage from "../components/LoadingPage";
import {PhotoViewer} from "../components/PhotoViewer";


export class MapSquareView extends PhotoViewer {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            mapSquareData: null
        };
    }

    async componentDidMount() {
        try {
            const response = await fetch(`/api/map_square/${this.props.mapSquareNumber}/`);
            if (!response.ok) {
                this.setState({loading: false});
            } else {
                const mapSquareData = await response.json();
                this.setState({
                    mapSquareData,
                    loading: false
                });
                console.log("mapSquareData", mapSquareData);
            }
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        if (this.state.loading) {
            return (<LoadingPage/>);
        }
        if (!this.state.mapSquareData) {
            return (<>
                Map Square {this.props.mapSquareNumber} is not in database.
            </>);
        }
        const {
            number,
            photos
        } = this.state.mapSquareData;

        return (<>
            <Navbar/>
            <div className="page">
                <h1>Map Square {number}</h1>
                {photos.length
                    ? (<>{
                        this.getPhotoGrid(photos, {"photoSize": [120, 120]})
                    }</>)
                    : "No metadata has been transcribed for these photos."
                }
            </div>
            <Footer/>
        </>);
    }
}

MapSquareView.propTypes = {
    mapSquareNumber: PropTypes.number
};
