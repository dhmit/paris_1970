import React from 'react';
import { Navbar, Footer } from '../UILibrary/components';
// import PropTypes from 'prop-types';

export class Search extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            data: null,
        };
    }

    async componentDidMount() {
        // try {
        //     const apiURL = '/api/something';
        //     const response = await fetch(apiURL);
        //     if (!response.ok) {
        //         this.setState({ loading: false });
        //     } else {
        //         const data = await response.json();
        //         this.setState({
        //             data,
        //             loading: false,
        //         });
        //     }
        // } catch (e) {
        //     console.log(e);
        // }
    }

    render() {
        return (
            <>
                <Navbar />
                <div className='page'>
                    <h1>Search!</h1>
                </div>
                <Footer />
            </>

        );
    }
}
