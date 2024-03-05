import React from "react";
import * as PropTypes from "prop-types";

import PhotoViewer from "../components/PhotoViewer";
import LoadingPage from "./LoadingPage";
import { Trans, withTranslation } from "react-i18next";


class BaseMapSquareView extends PhotoViewer {
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
            return (<Trans
                i18nKey='MapSquare.notInDB'
                values={{ squareNum: this.props.mapSquareNumber }}
            />);
        }
        const {
            number,
            photos
        } = this.state.mapSquareData;

        return (<>
            <div className="page">
                <h1>{`${this.props.t('global.mapSquare')} ${number}`}</h1>
                <ul className={"list-inline"}>
                    {photos.length
                    ? (<>{
                        this.getPhotoGrid(photos, {"photoSize": [120, 120]})
                    }</>)
                    : this.props.t('MapSquare.noMetadata')
                }</ul>
            </div>
        </>);
    }
}

BaseMapSquareView.propTypes = {
    mapSquareNumber: PropTypes.number
};

export const MapSquareView = withTranslation()(BaseMapSquareView);