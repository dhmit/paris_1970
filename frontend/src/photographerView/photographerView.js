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
                <ul className='photo-list'>
                    {photos.map((photo, k) => (
                        <li key={k}>
                            <a href={`/photo/${mapSquare.number}/${photo.number}/`}>
                                <h3>Photo {photo.id}</h3>
                            </a>
                        </li>
                    ))}
                </ul>
            </div>
            <Footer/>
        </>);
    }
}
PhotographerView.propTypes = {
    photographerNumber: PropTypes.number,
};
