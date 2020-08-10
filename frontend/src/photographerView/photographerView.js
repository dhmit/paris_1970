import React from 'react';
import * as PropTypes from 'prop-types';
import Navbar from '../about/Navbar';
import { Footer } from '../UILibrary/components';


export class PhotographerView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photographer_data: null,
        };
    }

    async componentDidMount() {
        try {
            const photographerId = window.location.pathname.split('/')[2];
            const response = await fetch(`/api/photographer/${photographerId}/`);
            if (!response.ok) {
                this.setState({ loading: false });
            } else {
                const photographer_data = await response.json();
                this.setState({
                    photographer_data,
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
        if (!this.state.photographer_data) {
            return (<>
                Photographer with primary
                key {window.location.pathname.split('/')[2]} not in database.
            </>);
        }
        const {
            name,
            map_square,
            number,
            sentiment,
            type,
            photos,
        } = this.state.photographer_data;

        return (<>
            <Navbar/>
            <div className='page'>
                <div className='photographer-name'>
                    {name} (ID: {number})
                </div>
                <div className='photographer-mapsquare'>
                    Assigned to Map Square {map_square.number}
                </div>
                <div className='photographer-sentiment'>
                    Sentiment on Paris: {sentiment === '' ? 'N/A' : sentiment }
                </div>
                <div className='photographer-type'>
                    Type of Photographer: {type === '' ? 'N/A' : type }
                </div>
                <div className='photographer-photos'>
                    Photos:
                    <ul className='photo-list'>
                        {photos.map((photo, k) => (
                            <li key={k}>
                                <a href={`/photos/${photo.id}`}>
                                    <h3>Photo {photo.id}</h3>
                                </a>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
            <Footer/>
        </>);
    }
}
PhotographerView.propTypes = {
    id: PropTypes.number,
};
