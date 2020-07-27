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
            photo_data: null,
        };
    }

    async componentDidMount() {
        try {
            const response = await fetch('/api/all_photos/');
            const photo_data = await response.json();
            this.setState({ photo_data, loading: false });
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        if (!this.state.photo_data) {
            return (<>
                Loading...
            </>);
        }
        return (<>
            <div className='landing-page'>
                <Navbar/>
                <div className="row" >
                    <div className='col-lg-6 col-md-12'>
                        Hello, World!
                    </div>
                    <div className='col-lg-12 col-md-12'>
                        {this.state.photo_data.map((photo, k) => (
                            <a key={k} href={`/photos/${photo.id}`}>
                                <h3>{photo.title}</h3>
                                <img width={500} height={500} src={photo.src} alt={photo.alt}/>
                            </a>
                        ))}
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
