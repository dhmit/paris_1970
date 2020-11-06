import React from 'react';
import * as PropTypes from 'prop-types';

import Navbar from '../about/navbar';
import { Footer } from '../UILibrary/components';

export class PhotographerView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photographerData: null,
        };
    }

    async componentDidMount() {
        try {
            const response = await fetch(`/api/photographer/${this.props.photographerNumber}/`);
            if (!response.ok) {
                this.setState({ loading: false });
            } else {
                const photographerData = await response.json();
                this.setState({
                    photographerData,
                    loading: false,
                });
            }
        } catch (e) {
            console.log(e);
        }
    }

    getAggregatePhotoAnalysis = (photos) => {
        console.log(photos);
    };

    render() {
        if (this.state.loading) {
            return (<>
                Loading!
            </>);
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
            sentiment,
            type,
            photos,
        } = this.state.photographerData;

        // const photographerAnalysis = this.getAggregatePhotoAnalysis(photos);
        return (<>
            <Navbar/>
            <div className='page'>
                <h1>{name} (ID: {number})</h1>
                <h3>Assigned to:</h3>
                <h5>Map Square {mapSquare.number}</h5>
                <h3 className='photographer-heading'>Sentiment on Paris:</h3>
                <h5>{sentiment === '' ? 'N/A' : sentiment }</h5>
                <h3>Type of Photographer:</h3>
                <h5>{type === '' ? 'N/A' : type }</h5>
                <h3>Photos:</h3>
                <div className='photo_gallery'>
                    {photos.map((photo, k) => (
                        <div className="photo" key={k}>
                            <a
                                key={k}
                                href={`/photo/${photo['map_square_number']}/${photo['number']}/`}
                            >
                                <img
                                    alt={photo.alt}
                                    height={200}
                                    width={200}
                                    src={photo['thumbnail_src']}
                                />
                            </a>
                        </div>
                    ))}
                </div>
            </div>
            <Footer/>
        </>);
    }
}
PhotographerView.propTypes = {
    photographerNumber: PropTypes.number,
};
