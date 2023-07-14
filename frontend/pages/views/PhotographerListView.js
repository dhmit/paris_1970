import React from "react";
import Footer from "../../components/Footer";
import * as PropTypes from "prop-types";
import { debounce } from "../../common";

import Chevron from "../../images/icons/chevron_down.svg";
import RedBlueBox from "../../images/icons/red_blue_box.svg";
import RedBlueBoxUrl from "../../images/icons/red_blue_box.svg?url";

// Change this value to more realisitic values that can replace the actual ones in case of error
const initialDropdownOptions = {
    locations: ["1", "2", "3"],
    squares: ["1", "2", "3"],
    nameStartsWith: ["A", "B", "..."],
    orderBy: ["name asc", "name desc", "..."],
};
class DropDown extends React.Component {
    constructor(props) {
        super(props);
        this.wrapperRef = React.createRef();
    }


    render() {
        return (
            <div
                ref={this.wrapperRef}
                className="dropdown-container"
                onClick={() => {
                    if (this.props.activeDropdown === this.props.id) {
                        this.props.toggleActiveDropdown(null);
                    } else {
                        this.props.toggleActiveDropdown(this.props.id);
                    }
                }}
            >
                <div
                    className={`dropdown-select ${this.props.blue ? "blue-border" : "red-border"}`}
                >
                    <p>{this.props.value || this.props.placeholder}</p>
                    <Chevron />
                </div>
                <div className="dropdown-spacer"></div>
                <div
                    className={`dropdown-items ${
                        this.props.id === this.props.activeDropdown ? "" : "d-none"
                    }`}
                    id={this.props.id}
                >
                    {this.props.items.map((item) => {
                        return (
                            <div
                                key={item}
                                className={`dropdown-itm ${
                                    this.props.value === item ? "selected-itm" : "unselected-itm"
                                }`}
                                onClick={(e) => {
                                    e.stopPropagation();
                                    if (this.props.value !== item) {
                                        this.props.onChange(item);
                                    } else {
                                        this.props.onChange("");
                                    }
                                }}
                            >
                                {item}
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    }
}

export class PhotographerListView extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            timer: null,
            searchQueries: { name: "", location: "", square: "", nameStartsWith: "" },
            activeDropdown: null,
            photographers: [],
            pageNumber: 1,
            isLastPage: false,
            sortBy: "",
            dropdownSearchOptions: initialDropdownOptions,
            toggleFilter: false,
        };
        this.refetchPhotographers = this.refetchPhotographers.bind(this);
        this.loadDropdownSearchOptions = this.loadDropdownSearchOptions.bind(this);
        this.resetPaginationParameters = this.resetPaginationParameters.bind(this);
        this.handleScroll = this.handleScroll.bind(this);
    }

    async loadDropdownSearchOptions() {
        const fetchOptions = async () => {
            try {
                const res = await fetch("/api/search_photographers/dropdown_options");
                return res.json();
            } catch {
                console.log("ERROR FETCHING OPTIONS FOR DROPDOWN SEARCH");
                return initialDropdownOptions;
            }
        };
        const searchOptions = await fetchOptions();
        this.setState({ dropdownSearchOptions: searchOptions });
    }

    refetchPhotographers() {
        const fetchPhotographers = async (searchQueries, orderBy) => {
            if (this.state.isLastPage) {
                return;
            }
            const { name, nameStartsWith, location, square } = searchQueries;
            const newPageNumber = this.state.pageNumber + 1;
            try {
                const res = await fetch(
                    `/api/search_photographers?
						name=${!name ? "" : name}&
						location=${!location ? "" : location}&
						name_starts_with=${!nameStartsWith ? "" : nameStartsWith}&
						square=${square === "" || square === undefined || square === null ? "" : square}&
						order_by=${!orderBy ? "" : orderBy}&
						page=${newPageNumber}
					`
                );
                return res.json();
            } catch {
                return [];
            }
        };
        debounce(async () => {
            try {
                const { results, is_last_page, page_number } = await fetchPhotographers(
                    this.state.searchQueries,
                    this.state.sortBy
                );
                this.setState({
                    photographers: this.state.photographers.concat(results),
                    isLastPage: is_last_page,
                    pageNumber: parseInt(page_number),
                });
            } catch (err) {
                console.log(err);
                console.log("Error fetching page!!!");
            }
        }, 300)();
    }

    getPhotoList() {
        const photoSize = [100, 100];

        console.log(this.state.photographers);

        const photoList = this.state.photographers.map((photographer, k) => {
            const examplePhotoSrc = photographer.example_photo_src;
            let imgElement;

            if (examplePhotoSrc) {
                const altText = `An example photograph by ${photographer.name}`;
                imgElement = (
                    <img alt={altText} width={photoSize[0]} src={photographer.example_photo_src} />
                );
            } else {
                const altText =
                    "A placeholder image because an example photograph by " +
                    `${photographer.name} is missing.`;
                imgElement = <img alt={altText} width={photoSize[0]} src={RedBlueBoxUrl} />;
            }

            return (
                <li className="one-photographer list-inline-item" key={k}>
                    <a key={k} href={`/photographer/${photographer.number}`}>
                        {imgElement}
                    </a>
                    <p>{photographer.name ? photographer.name : "No Name"}</p>
                </li>
            );
        });

        return photoList;
    }

    searchQueryChanged(oldQuery, newQuery) {
        return (
            oldQuery.name !== newQuery.name ||
            oldQuery.nameStartsWith !== newQuery.nameStartsWith ||
            oldQuery.square !== newQuery.square ||
            oldQuery.location !== newQuery.location
        );
    }

    handleScroll(e) {
        // doing some arithmetic with the scroll height here to detect when the user reaches the bottom of the list
        console.log(e.target.scrollHeight, e.target.clientHeight, e.target.scrollTop);
        const bottom =
            Math.trunc((e.target.scrollHeight - e.target.clientHeight) / 10) <=
            Math.trunc(e.target.scrollTop / 10);

        // if we reach bottom we load the next page of photographers
        if (bottom) {
            console.log("reached end of page");
            if (!this.state.isLastPage) {
                this.refetchPhotographers();
            }
        }
    }

    resetPaginationParameters() {
        this.setState({ pageNumber: 0, isLastPage: false, photographers: [] });
    }

    toggleActiveDropdown = (dropDown) => {
        this.setState({ activeDropdown: dropDown });
    };

    componentDidMount() {
        this.loadDropdownSearchOptions();
        this.refetchPhotographers();
    }

    componentDidUpdate(prevProps, prevState) {
        if (
            this.searchQueryChanged(prevState.searchQueries, this.state.searchQueries) ||
            this.state.sortBy !== prevState.sortBy
        ) {
            this.resetPaginationParameters();
            this.refetchPhotographers();
        }
    }

    render() {
        return (
            <div className="photographerList-container">
                <div id={"banner"}>
                    <div className="header">
                        <div className="red-blue-box">
                            <RedBlueBox />
                        </div>
                        <p className="heading">Photographers</p>
                    </div>

                    {/* onClick toggle visibility of filter container */}
                    <div className="filter-btn-container">
                        <button
                            className="primary-btn"
                            onClick={() => {
                                this.setState({
                                    toggleFilter: !this.state.toggleFilter,
                                });
                            }}
                        >
                            {this.state.toggleFilter ? "Hide Filters" : "Show Filters"}
                        </button>
                    </div>

                    {this.state.toggleFilter && (
                        <form id={"filterContainer"}>
                            <input
                                type="text"
                                id="photographerList-search"
                                placeholder="Search by name"
                                onChange={(e) => {
                                    this.setState((prev) => ({
                                        searchQueries: {
                                            ...prev.searchQueries,
                                            name: e.target.value,
                                        },
                                    }));
                                }}
                                value={this.state.name}
                            />
                            <div className="advancedSearch-container">
                                <div className="filterBy-container">
                                    <p>Filter by:</p>
                                    <div className="filters-container">
                                        <DropDown
                                            id="loc-filter"
                                            blue={true}
                                            items={this.state.dropdownSearchOptions.locations}
                                            placeholder={"Locations"}
                                            activeDropdown={this.state.activeDropdown}
                                            toggleActiveDropdown={this.toggleActiveDropdown}
                                            onChange={(value) => {
                                                this.setState((prev) => ({
                                                    searchQueries: {
                                                        ...prev.searchQueries,
                                                        location: value,
                                                    },
                                                }));
                                            }}
                                            value={this.state.searchQueries.location}
                                        />
                                        <DropDown
                                            id="sq-filter"
                                            blue={true}
                                            items={this.state.dropdownSearchOptions.squares}
                                            placeholder={"Map Square"}
                                            activeDropdown={this.state.activeDropdown}
                                            toggleActiveDropdown={this.toggleActiveDropdown}
                                            value={this.state.searchQueries.square}
                                            onChange={(value) => {
                                                this.setState((prev) => ({
                                                    searchQueries: {
                                                        ...prev.searchQueries,
                                                        square: value,
                                                    },
                                                }));
                                            }}
                                        />
                                        <DropDown
                                            id="alph-filter"
                                            blue={true}
                                            items={this.state.dropdownSearchOptions.nameStartsWith}
                                            placeholder={"Alphabet"}
                                            activeDropdown={this.state.activeDropdown}
                                            toggleActiveDropdown={this.toggleActiveDropdown}
                                            value={this.state.searchQueries.nameStartsWith}
                                            onChange={(value) => {
                                                this.setState((prev) => ({
                                                    searchQueries: {
                                                        ...prev.searchQueries,
                                                        nameStartsWith: value,
                                                    },
                                                }));
                                            }}
                                        />
                                    </div>
                                </div>
                                <div className="filterBy-container">
                                    <p>Sort by:</p>
                                    <DropDown
                                        id="sort"
                                        blue={false}
                                        items={this.state.dropdownSearchOptions.orderBy}
                                        placeholder={"---"}
                                        activeDropdown={this.state.activeDropdown}
                                        toggleActiveDropdown={this.toggleActiveDropdown}
                                        value={this.state.sortBy}
                                        onChange={(value) => {
                                            this.setState({
                                                sortBy: value,
                                            });
                                        }}
                                    />
                                </div>
                            </div>
                        </form>
                    )}
                </div>

                <div className="photographerGallery" onScroll={this.handleScroll}>
                    <div id="overlay"></div>

                    <ul className="list-inline" >
                        {this.getPhotoList()}
                        <div className="photographers-results-footer">
                            {this.state.isLastPage
                                ? this.state.photographers.length === 0
                                    ? "No photographers found that match your search query!"
                                    : "End of Results!!!"
                                : "Loading..."}
                        </div>
                    </ul>
                </div>
                <div className="footer-container mb-3">
                    <Footer />
                </div>
            </div>
        );
    }
}

PhotographerListView.propTypes = {
    photoListDir: PropTypes.string,
    photographers: PropTypes.string,
};

DropDown.propTypes = {
    id: PropTypes.string,
    blue: PropTypes.bool,
    items: PropTypes.array,
    placeholder: PropTypes.string,
    toggleActiveDropdown: PropTypes.func,
    activeDropdown: PropTypes.string,
    onChange: PropTypes.func,
    value: PropTypes.any,
};
