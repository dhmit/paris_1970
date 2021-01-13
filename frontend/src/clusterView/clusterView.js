import React from 'react';
import * as PropTypes from 'prop-types';

import { Navbar, Footer } from '../UILibrary/components';

const SIDES = {
    CLEANED: 'cleaned',
    FRONT: 'front',
    BACK: 'back',
    BINDER: 'binder',
};


export class ClusterView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photoData: null,
        };
    }

    async componentDidMount() {
        try {
            const apiURL = '/api/clustering/'
                + `${this.props.numberOfClusters}/${this.props.clusterNumber}/`;
            console.log(apiURL);
            const response = await fetch(apiURL);
            if (!response.ok) {
                this.setState({ loading: false });
            } else {
                const photoData = await response.json();
                this.setState({
                    photoData,
                    loading: false,
                });
            }
        } catch (e) {
            console.log(e);
        }
    }

    getSource(photoData) {
        const availableSides = Object.values(SIDES).filter(
            (side) => photoData[`${side}_src`] !== null,
        );
        const displaySide = availableSides.length > 0 ? availableSides[0] : '';
        const source = photoData[`${displaySide}_src`];
        const fileId = source.split('=')[1];
        const thumbnail = `https://drive.google.com/thumbnail?authuser=0&sz=w100&id=${fileId}`;
        return thumbnail;
    }

    render() {
        if (this.state.loading) {
            return (<h1>
                Loading!
            </h1>);
        }

        console.log(this.state.photoData);
        const photos = this.state.photoData.map((photo, k) => {
            return (
                <a
                    key={k}
                    href={`/photo/${photo['map_square_number']}/${photo['number']}/`}
                >
                    <img
                        alt={photo.alt}
                        height={100}
                        width={100}
                        src={this.getSource(photo)}
                    />
                </a>
            );
        });

        const prevButton = this.props.clusterNumber - 1 >= 0 ? (
            <a
                title='prev'
                href={`/clustering/${this.props.numberOfClusters}/${this.props.clusterNumber - 1}/`}
            >
                <button className='order-button'>
                    Prev
                </button>
            </a>) : (<></>);

        const nextButton = this.props.clusterNumber + 1 < this.props.numberOfClusters ? (
            <a
                title='next'
                href={`/clustering/${this.props.numberOfClusters}/${this.props.clusterNumber + 1}/`}
            >
                <button className='order-button'>
                    Next
                </button>
            </a>) : (<></>);

        const options = this.state.photoData.length === 0 ? (
            <p>
                {`There are no photos that are in cluster ${this.props.clusterNumber}`
                + ' or the cluster number is out of bounds.'}
            </p>) : (<div className='state-buttons row'>{prevButton}{nextButton}</div>);

        return (<>
            <Navbar />
            <div className='display-box page'>
                <h3>
                    Number of clusters: {this.props.numberOfClusters + ' '}
                    Cluster number: {this.props.clusterNumber}
                </h3>
                {options}
                <br/>
                {photos}
            </div>
            <Footer />
        </>);
    }
}
ClusterView.propTypes = {
    numberOfClusters: PropTypes.number,
    clusterNumber: PropTypes.number,
};
