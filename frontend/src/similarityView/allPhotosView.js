import React from 'react';

import Navbar from '../about/navbar';
import { Footer, LoadingPage } from '../UILibrary/components';

const SIDES = {
    CLEANED: 'cleaned',
    FRONT: 'front',
    BACK: 'back',
    BINDER: 'binder',
};

// TODO: fix similarityView, photos don't show

export class AllPhotosView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photoData: null,
            displayOrder: 'Ascending',
        };
    }

    async componentDidMount() {
        try {
            const apiURL = '/api/all_photos';
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

    reverseOrder = () => {
        let newOrder;
        if (this.state.displayOrder === 'Descending') {
            newOrder = 'Ascending';
        } else {
            newOrder = 'Descending';
        }
        const newPhotoData = this.state.photoData.reverse();
        this.setState({
            photoData: newPhotoData,
            displayOrder: newOrder,
        });
    };

    getSource(photoData) {
        const availableSides = Object.values(SIDES).filter(
            (side) => photoData[`${side}_src`] !== null,
        );
        const displaySide = availableSides.length > 0 ? availableSides[0] : '';
        const source = photoData[`${displaySide}_src`];
        return source;
    }

    render() {
        if (this.state.loading) {
            return (<LoadingPage/>);
        }

        const photos = this.state.photoData.map((photo, k) => {
            /* const currentAnalysis = photo['analyses'].filter(
                (analysisObject) => analysisObject.name === 'resnet18_cosine_similarity',
            )[0]; */
            return (
                <a
                    key={k}
                    title={`Map Square: ${photo['map_square_number']},\nPhoto: ${photo['number']}`}
                    href={`/similar_photos/${photo['map_square_number']}/${photo['number']}/`}
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

        const options = this.state.photoData.length === 0 ? (
            <p>
                {'There are no photos that have an analysis result for resnet18_cosine_similarity'
                + ' or the analysis does not exist.'}
            </p>) : (<div className='options'>
            <p>Click on a photo to see the 10 most similar matches!</p></div>);

        return (<>
            <Navbar />
            <div className='display-box page'>
                <h3 className='text-capitalize'>{
                    'resnet18_cosine_similarity'
                }</h3>
                {options}
                <br/>
                {photos}
            </div>
            <Footer />
        </>);
    }
}
