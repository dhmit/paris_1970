import React from 'react';
import { Navbar, Footer } from '../UILibrary/components';
// import PropTypes from 'prop-types';

class SearchForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: ''};

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({value: event.target.value});
    }

    handleSubmit(event) {
        event.preventDefault();
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    <input type="text" value={this.state.value} onChange={this.handleChange} />
                </label>
                <input type="submit" value="Search" />
            </form>
        );
    }
}

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
                    <SearchForm />
                </div>
                <Footer />
            </>

        );
    }
}
