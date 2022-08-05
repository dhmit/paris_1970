import React from "react";
import PropTypes from "prop-types";

import PhotoViewer from "../components/PhotoViewer";
import SearchIcon from "../images/icons/search.svg";
import SearchBgTopLeft from "../images/search_top_left.svg";
import SearchBgTopRight from "../images/search_top_right.svg";


class SearchBar extends React.Component {
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
        window.addEventListener(
            "keydown",
            (e) => e.code.indexOf("Enter") >= 0 ? this.handleSubmit(e) : null
        );

        return (
            <div className="search-bar">
                <div className="search-icon"><SearchIcon/></div>
                <input
                    className="form-control"
                    type="text"
                    name="keywords"
                    value={this.state.keywords}
                    onChange={this.handleChange}
                />
                <button
                    className="btn"
                    onClick={this.handleSubmit}>
                    Advanced Search
                </button>
            </div>
        );
    }
}

SearchBar.propTypes = {
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
        return (<>
            <div className="search-page page row">
                <div className="search-container">
                    <SearchBgTopLeft className="search-bg-image-left"/>
                    <SearchBgTopRight className="search-bg-image-right"/>
                    <div className="row height d-flex justify-content-center align-items-center">
                        <div className="col-md-8">
                            <SearchBar updateSearchData={this.updateSearchData}/>
                        </div>
                    </div>
                </div>
                {
                    this.state.data &&
                    <div className="search-container">
                        <p>{this.state.searchText}</p>
                        <ul className="list-inline earch-photo-container">
                            {this.getPhotoGrid(
                                this.state.data,
                                {"className": "search-photo", "photoSize": [140, 140]}
                            )}
                        </ul>
                    </div>
                }
            </div>
        </>);
    }
}
