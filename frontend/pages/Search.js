import React from "react";
import PropTypes from "prop-types";

import PhotoViewer from "../components/PhotoViewer";
import SearchIcon from "../images/icons/search.svg";
import SearchBgTopLeft from "../images/search_top_left.svg";
import SearchBgTopRight from "../images/search_top_right.svg";

import DropdownButton from "react-bootstrap/DropdownButton";
import Badge from "react-bootstrap/Badge";

class SearchBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tags: [],
            arrondissements: [],
        };
    }

    handleSearch = async (body) => {
        const searchResponse = await fetch(`/api/search/`);
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
        return (<>
            <div className="search-bar">
                <div className="search-icon"><SearchIcon /></div>
                <input
                    className="form-control"
                    type="text"
                    name="keywords"
                    value={this.state.keywords}
                    onChange={this.handleChange} />

            </div>
            <div>
                <FilterBar keyWords={this.state.keywords} updateSearchData={this.props.updateSearchData}/>
            </div>
        </>);
    }
}

SearchBar.propTypes = {
    updateSearchData: PropTypes.func
};

class FilterBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {

        };
        this.handleCheckboxChange = this.handleCheckboxChange.bind(this);
    }

    handleCheckboxChange = (event) => {
        const target = event.target;
        const checked = target.checked;
        const name = target.name;
        this.setState({
            [name]: checked,
        });
    };

    handleApply = async () => {
        const filters = [];
        for (const e in this.state){
            if (this.state[e]){
                filters.push(e);
            }
        }
        const allTags = this.props.keyWords.trim() + " " + filters.join(" ");
        console.log(allTags);
        const searchResponse = await fetch(`/api/search/?query=${JSON.stringify(allTags)}`);
        const {
            keywords,
            searchData
        } = await searchResponse.json();
        let searchText = searchData.length + " photographs";
        if (allTags) {
            searchText += " found with keywords: " + keywords;
        }
        this.props.updateSearchData({
            data: searchData,
            searchText
        });
    };

    handleClear = async (event) => {
        event.preventDefault();
        //something
    };

    render() {
        return (
            <div className="checkbox-bar">
                    <h1>
                        <Badge bg="light" text="dark">
                            Filter by:
                        </Badge>
                    </h1>

                    <DropdownButton className="dropdown" id="dropdown-basic-button" title="Vehicles">
                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Car"
                                onChange={this.handleCheckboxChange}/>
                                Car
                            </label>
                        </li>

                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Motorcycle"
                                onChange={this.handleCheckboxChange}/>
                                Motorcycle
                            </label>
                        </li>

                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Truck"
                                onChange={this.handleCheckboxChange}/>
                                Truck
                            </label>
                        </li>

                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Boat"
                                onChange={this.handleCheckboxChange}/>
                                Boat
                            </label>
                        </li>

                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Airplane"
                                onChange={this.handleCheckboxChange}/>
                                Airplane
                            </label>
                        </li>

                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Bicycle"
                                onChange={this.handleCheckboxChange}/>
                                Bicycle
                            </label>
                        </li>
                    </DropdownButton>

                    <DropdownButton className="dropdown" id="dropdown-basic-button" title="City Features">
                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Light"
                                onChange={this.handleCheckboxChange}/>
                                Traffic Light
                            </label>
                        </li>

                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Stop Sign"
                                onChange={this.handleCheckboxChange}/>
                                Stop Sign
                            </label>
                        </li>

                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Bench"
                                onChange={this.handleCheckboxChange}/>
                                Bench
                            </label>
                        </li>

                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Clock"
                                onChange={this.handleCheckboxChange}/>
                                Clock
                            </label>
                        </li>

                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Chair"
                                onChange={this.handleCheckboxChange}/>
                                Chair
                            </label>
                        </li>
                    </DropdownButton>

                    <DropdownButton className="dropdown" id="dropdown-basic-button" title="Miscellaneous">
                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Person"
                                onChange={this.handleCheckboxChange}/>
                                Person
                            </label>
                        </li>

                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Potted Plant"
                                onChange={this.handleCheckboxChange}/>
                                Potted Plant
                            </label>
                        </li>

                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Handbag"
                                onChange={this.handleCheckboxChange}/>
                                Handbag
                            </label>
                        </li>

                        <li>
                            <label>
                                <input
                                type="checkbox"
                                name="Cat"
                                onChange={this.handleCheckboxChange}/>
                                Cat
                            </label>
                        </li>
                    </DropdownButton>

                    <button
                        className="applybtn"
                        onClick={this.handleApply}>
                        Apply Filters
                    </button>

                    <button
                        className="clearnbtn"
                        onClick={this.handleClear}>
                        Clear Filters
                    </button>
                </div>
            );
        }
    }

export class Search extends PhotoViewer {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            data: null,
            searchedText: ""
        };
    }

    render() {
        return (<>
            <div className="row">
                <SearchBgTopLeft className="search-bg-image-left"/>
                <SearchBgTopRight className="search-bg-image-right"/>
                <div className="row height d-flex justify-content-center align-items-center">
                    <div className="col-md-8">
                        <SearchBar updateSearchData={this.updateSearchData}/>
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
