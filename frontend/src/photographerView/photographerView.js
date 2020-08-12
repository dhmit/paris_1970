import React from 'react';
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
                <h1>{name} (ID: {number})</h1>
                <h3>Assigned to:</h3>
                <h5>Map Square {map_square.number}</h5>
                <h3 className='photographer-heading'>Sentiment on Paris:</h3>
                <h5>{sentiment === '' ? 'N/A' : sentiment }</h5>
                <h3>Type of Photographer:</h3>
                <h5>{type === '' ? 'N/A' : type }</h5>
                <h3>Photos:</h3>
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
            <Footer/>
        </>);
    }
}