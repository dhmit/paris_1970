import React from 'react';
import * as PropTypes from 'prop-types';
import Navbar from '../about/Navbar';
import { Footer } from '../UILibrary/components';


export class PhotoView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photo_data: null,
        };
    }

    async componentDidMount() {
        try {
            const photoId = this.props.id;
            const response = await fetch(`/api/photo/${photoId}/`);
            if (!response.ok) {
                this.setState({ loading: false });
            } else {
                const photo_data = await response.json();
                this.setState({ photo_data, loading: false });
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
        if (!this.state.photo_data) {
            return (<>
                Photo with id {this.props.id} is not in database.
                <a href={`/photos/${this.props.id - 1}/`}>Prev</a>
                <br/>
                <a href={`/photos/${this.props.id + 1}/`}>Next</a>
            </>);
        }
        const {
            title,
            alt,
            front_src,
            back_src,
        } = this.state.photo_data;

        console.log(this.state.photo_data);

        return (<>
            <Navbar />
            <div style={{ padding: '100px 50px' }}>
                <h2>{title}</h2>
                <img width={500} height={500} src={front_src} alt={alt}/>
                <img width={500} height={500} src={back_src} alt={alt}/>
                <br/>
                <a href={`/photos/${this.props.id - 1}/`}>Prev</a>
                <br/>
                <a href={`/photos/${this.props.id + 1}/`}>Next</a>
            </div>
            <Footer />
        </>);
    }
}
PhotoView.propTypes = {
    id: PropTypes.number,
};
