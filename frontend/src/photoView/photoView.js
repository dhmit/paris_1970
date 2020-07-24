import React from 'react';
// import * as PropTypes from 'prop-types';
import Navbar from '../about/Navbar';
import { Footer } from '../UILibrary/components';


const PROTOTYPING_FAKE_DATA = {
    title: 'some title',
    src: 'img_src.jpg',
    alt: 'image alt text',
};

export class PhotoView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            photo_data: null,
        };
    }

    componentDidMount() {
        // TODO: get data from the backend instead of faking it
        this.setState({
            photo_data: PROTOTYPING_FAKE_DATA,
        });
    }

    render() {
        if (!this.state.photo_data) {
            return (<>
                Loading!
            </>);
        }
        const src = this.state.photo_data.src;
        const alt = this.state.photo_data.alt;
        const title = this.state.photo_data.title;

        return (<>
            <Navbar />
            <div style={{ height: '75px' }}>-</div>
            <p>Hello world.</p>
            <img src={src} alt={alt}/>
            <p>{title}</p>
            <Footer />
        </>);
    }
}
