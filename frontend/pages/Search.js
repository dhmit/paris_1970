import React from "react";
import PropTypes from "prop-types";

import Footer from "../components/Footer";
import PhotoViewer from "../components/PhotoViewer";


class SearchForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            keywords: ""
        };
    }

    handleChange = (event) => {
        this.setState({
            [event.target.name]: event.target.value
        });
    };

    handleSearch = async (body) => {
        const searchResponse = await fetch(`/api/search/?query=${JSON.stringify(body)}`);
        console.log("Called handle search");
        const {
            keywords,
            searchData
        } = await searchResponse.json();
        let searchText = searchData.length + " photographs";
        if (body.keywords) {
            searchText += " found with keywords: " + keywords;
        }
        this.props.updateSearchData({
            data: searchData,
            searchText
        });
    };

    handleSubmit = async (event) => {
        event.preventDefault();
        if (this.state.keywords) {
            await this.handleSearch({
                keywords: this.state.keywords.trim()
            });
        }
    };

    render() {
        return (
            <div>
                {/* Full-Text Form */}
                <form onSubmit={this.handleSubmit}>
                    <h3>Full Text Search</h3>
                    <label className="input-div">
                        <input
                            className="search-text-input"
                            type="text"
                            name="keywords"
                            value={this.state.keywords}
                            onChange={this.handleChange}
                        />
                    </label>
                    <br/>
                    <input type="submit" value="Search"/>
                </form>
            </div>
        );
    }
}

SearchForm.propTypes = {
    updateSearchData: PropTypes.func
};

export class Search extends PhotoViewer {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            data: null,
            searchedText: ""
        };
    }

    updateSearchData = (searchData) => {
        this.setState({...searchData});
    };

    // Full text + advanced search model: http://photogrammar.yale.edu/search/
    render() {
        return (
            <>
                <div className="search-page page row">
                    <div className="col-sm-12 col-lg-4 search-form">
                        <h1>Search</h1>
                        <SearchForm
                            updateSearchData={this.updateSearchData}
                        />
                    </div>
                    <div className="col-sm-12 col-lg-8">
                        {
                            this.state.data &&
                            <div>
                                <p>{this.state.searchText}</p>
                                <div className="search-results">
                                    {this.getPhotoGrid(
                                        this.state.data, {"photoSize": [120, 120]}
                                    )}
                                </div>
                            </div>
                        }
                    </div>
                </div>
                <Footer/>
            </>
        );
    }
}
