import React from 'react';
import { Navbar, Footer } from '../UILibrary/components';
// import PropTypes from 'prop-types';

class SearchForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            keyword: '',
            photographer: '',
            caption: '',
            tags: '',
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({
            ...this.state,
            [event.target.name]: event.target.value
        });
    }

    handleSubmit(event) {
        event.preventDefault();
    }

    // When it comes to separating the advanced search and full text search ("normal" search),
    // should we split the two forms? I think this would work with the same submit button
    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <h3>Full Text Search</h3>
                <label>
                    <input type="text" name="keyword" value={this.state.keyword} onChange={this.handleChange} />
                </label>
                <input type="submit" value="Search" />
                <br/><br/>

                <h3>Advanced Search</h3>
                <label>
                    <p>Photographer:&nbsp;
                        <input type="text" name="photographer" value={this.state.photographer} onChange={this.handleChange} />
                    </p>
                </label>
                <br/>
                <label>
                    <p>Caption:&nbsp;
                        <input type="text" name="caption" value={this.state.caption} onChange={this.handleChange} />
                    </p>
                </label>
                <br/>
                <label>
                    <p>Tags:&nbsp;
                        <input type="text" name="tags" value={this.state.tags} onChange={this.handleChange} />
                    </p>
                </label>
                <br/>
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
        // this section implements the photographers view drop-down menu
        try {
            // do sth
            const photographersURL = 'api/'
        } catch (e) {
            console.log(e);
        }
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

    // This follows the full text + advanced search model here: http://photogrammar.yale.edu/search/
    render() {
        return (
            <>
                <Navbar />
                <div className='page'>
                    <h1>Search</h1>
                    <SearchForm />
                </div>
                <Footer />
            </>

        );
    }
}
