import React from 'react';
import * as PropTypes from 'prop-types';
import Navbar from '../about/Navbar';
import { Footer } from '../UILibrary/components';


export class PhotoView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            photo_data: null,
        };
    }

    async componentDidMount() {
        try {
            const photoId = this.props.id;
            const response = await fetch(`/api/photo/${photoId}/`);
            const photo_data = await response.json();
            this.setState({ photo_data });
        } catch (e) {
            console.log(e);
        }
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
            <img width={500} height={500} src={src} alt={alt}/>
            <p>{title}</p>
            <Footer />
        </>);
    }
}
PhotoView.propTypes = {
    id: PropTypes.number,
};
