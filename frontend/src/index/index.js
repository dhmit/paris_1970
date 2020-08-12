/*
  The landing page for the prototyping environment.
 *
 * PLEASE NOTE: this is not going to go into the EdX course.
 * It's just for our convenience while developing,
 * so DO NOT spend too much time making this nice!
 */

import React from 'react';
import * as PropTypes from 'prop-types';
import Navbar from '../about/Navbar';
import { Footer } from '../UILibrary/components';

export class IndexView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            map_data: null,
        };
    }

    async componentDidMount() {
        try {
            const map_response = await fetch('/api/all_map_squares/');
            const map_data = await map_response.json();
            this.setState({ map_data, loading: false });
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        if (!this.state.map_data) {
            return (<>
                Loading...
            </>);
        }
        const mapSquares = this.state.map_data.map((mapSquare, j) => {
            const pictureList = mapSquare.photos.map((photo, k) => (
                <li key={k} className='col-lg-12 col-md-12'>
                    <a href={`/photos/${photo.id}`}>
                        <h3>Photo{photo.id}</h3>
                    </a>
                </li>));
            return (<div key={j}>
                <a
                    href={`/map_square/${mapSquare.id}`}
                    className='map-square'
                >
                    {mapSquare.name}
                </a>

                <ul>{pictureList}</ul>
            </div>);
        });
        return (<>
            <div className='page'>
                <Navbar/>
                <div className="row" >
                    <div className='col-lg-12 col-md-12'>
                        {mapSquares}
                    </div>
                </div>
            </div>
            <Footer />
        </>);
    }
}

class IndexCard extends React.Component {
    render() {
        const createMarkup = () => {
            return { __html: this.props.description };
        };

        return (
            <div className='card mb-4 w-100'>
                <a className="text-dark" href={this.props.url}>
                    <div className='card-header'>{this.props.title} </div>
                </a>
                <div
                    className='card-body'
                    dangerouslySetInnerHTML={createMarkup()}
                />
            </div>
        );
    }
}
IndexCard.propTypes = {
    title: PropTypes.string,
    description: PropTypes.string,
    url: PropTypes.string,
};
