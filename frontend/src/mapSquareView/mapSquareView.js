import React from "react";
import * as PropTypes from "prop-types";

import {Navbar, Footer, LoadingPage} from "../UILibrary/components";
import {getSource} from "../analysisView/analysisView";

export class MapSquareView extends React.Component {
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
                console.log(mapSquareData);
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

        const photoListItem = (photo, k) => {
            const photoId = `${photo["map_square_number"]}/${photo["number"]}`;
            return (
                <a
                    key={k}
                    title={`Map Square: ${photo["map_square_number"]}` +
                    `, Number: ${photo["number"]}`}
                    href={"/photo/" + photoId + "/"}
                >
                    <img
                        alt={photo.alt}
                        height={120}
                        width={120}
                        src={getSource(photo)}
                    />
                </a>
            );
        };

        return (<>
            <Navbar/>
            <div className="page">
                <h1>Map Square {number}</h1>
                {photos.length
                    ? (<>{photos.map((photo, k) => photoListItem(photo, k))}</>)
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
