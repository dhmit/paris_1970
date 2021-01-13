import React from 'react';
import * as PropTypes from 'prop-types';

import Navbar from '../about/navbar';
import { Footer, Loading } from '../UILibrary/components';

export class MapSquareView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            mapSquareData: null,
        };
    }

    async componentDidMount() {
        try {
            const response = await fetch(`/api/map_square/${this.props.mapSquareNumber}/`);
            if (!response.ok) {
                this.setState({ loading: false });
            } else {
                const mapSquareData = await response.json();
                this.setState({
                    mapSquareData,
                    loading: false,
                });
                console.log(mapSquareData);
            }
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        if (this.state.loading) {
            return (
                <React.Fragment>
                    <Navbar />
                    <Loading/>
                    <Footer />
                </React.Fragment>
            );
        }
        if (!this.state.mapSquareData) {
            return (<>
                Map Square {this.props.mapSquareNumber} is not in database.
            </>);
        }
        const {
            number,
            photos,
        } = this.state.mapSquareData;

        const photoListItem = (photo, k) => {
            return (
                <li key={k}>
                    <a href={`/photo/${this.props.mapSquareNumber}/${photo.number}/`}>
                        <h3>Photo {photo.id}</h3>
                    </a>
                </li>
            );
        };

        return (<>
            <Navbar/>
            <div className="page">
                <h1>Map Square {number}</h1>
                { photos.length
                    ? (
                        <ul className='photo-list'>
                            {photos.map((photo, k) => photoListItem(photo, k))}
                        </ul>
                    )
                    : 'No metadata has been transcribed for these photos.'
                }
            </div>
            <Footer/>
        </>);
    }
}
MapSquareView.propTypes = {
    mapSquareNumber: PropTypes.number,
};
