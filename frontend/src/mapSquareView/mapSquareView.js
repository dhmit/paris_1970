import React from 'react';
import Navbar from '../about/navbar';
import { Footer } from '../UILibrary/components';

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
            const mapSquareId = window.location.pathname.split('/')[2];
            const response = await fetch(`/api/map_square/${mapSquareId}/`);
            if (!response.ok) {
                this.setState({ loading: false });
            } else {
                const mapSquareData = await response.json();
                this.setState({
                    mapSquareData,
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
        if (!this.state.mapSquareData) {
            return (<>
                Map Square with primary
                key {window.location.pathname.split('/')[2]} not in database.
            </>);
        }
        const {
            number,
            photos,
        } = this.state.mapSquareData;

        return (<>
            <Navbar/>
            <div className="page">
                <h1>Map Square {number}</h1>
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

