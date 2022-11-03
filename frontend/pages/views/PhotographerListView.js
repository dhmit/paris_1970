import React from "react";
import Footer from "../../components/Footer";
import * as PropTypes from "prop-types";
import { debounce } from "../../common";

import Chevron from "../../images/icons/chevron_down.svg";
import RedBlueBox from "../../images/icons/red_blue_box.svg";

const initialDropdownOptions = {
    locations: ["1", "2", "3"],
    squares: ["1", "2", "3"],
    nameStartWith: ["A", "B", "..."],
    orderBy: ["name asc", "name desc", "..."],
};
class DropDown extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selected: null,
        };

        this.wrapperRef = React.createRef();
        this.handleClickOutside = this.handleClickOutside.bind(this);
    }

    handleClickOutside() {
        if (this.wrapperRef && !this.wrapperRef.current.contains(event.target)) {
            this.props.toggleActiveDropdown(null);
        }
    }

    componentDidMount() {
        document.addEventListener("mousedown", this.handleClickOutside);
    }

    componentWillUnmount() {
        document.removeEventListener("mousedown", this.handleClickOutside);
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
                // onMouseEnter={() => {
                //     this.setState({toggleDropDown: true});
                //     let dropdowns = document.getElementsByClassName("dropdown-items");
                //     for (const elt of dropdowns) {
                //         if (elt.id !== this.props.id) {
                //             elt.classList.add("d-none");
                //         }
                //     }
                //     this.props.toggleActiveDropdown(this.props.id);
                // }}
                // onMouseLeave={() => {
                //     this.setState({toggleDropDown: false});
                //     this.props.toggleActiveDropdown(null);
                // }}
            >
                <div
                    className={`dropdown-select ${this.props.blue ? "blue-border" : "red-border"}`}
                >
                    <p>{this.state.selected || this.props.placeholder}</p>
                    <Chevron />
                </div>
                <div
                    className={`dropdown-items ${
                        this.props.id === this.props.activeDropdown ? "" : "d-none"
                    }`}
                    id={this.props.id}
                >
                    <div className="dropdown-spacer"></div>
                    {this.props.items.map((item) => {
                        return (
                            <div
                                key={item}
                                className={`dropdown-itm ${
                                    this.state.selected === item ? "selected-itm" : "unselected-itm"
                                }`}
                                onClick={() => {
                                    if (this.state.selected !== item) {
                                        this.setState({ selected: item });
                                    } else {
                                        this.setState({ selected: null });
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
            searchQueries: { name: "" },
            activeDropdown: null,
            photographers: [],
            pageNumber: 1,
            isLastPage: false,
            // These are dummy values. The actual value and options should be fetched from the backend
            dropdownSearchOptions: initialDropdownOptions,
        };
        this.refetchPhotographers = this.refetchPhotographers.bind(this);
        this.loadDropdownSearchOptions = this.loadDropdownSearchOptions.bind(this);
        this.resetPaginationParameters = this.resetPaginationParameters.bind(this);
        this.handleScroll = this.handleScroll.bind(this);
    }

    hrefFunc(number) {
        return `/photographer/${number}`;
    }

    srcFunc(number) {
        return `${this.props.photoListDir}/${number}_photo.jpg`;
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
        const fetchPhotographers = async (sq) => {
            if (this.state.isLastPage) {
                return;
            }
            const newPageNumber = this.state.pageNumber + 1;
            try {
                const res = await fetch(
                    `/api/search_photographers?name=${sq}&page=${newPageNumber}`
                );
                return res.json();
            } catch {
                return [];
            }
        };
        debounce(async () => {
            try {
                const { results, is_last_page, page_number } = await fetchPhotographers(
                    this.state.searchQueries.name
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
        return this.state.photographers.map((photographer, k) => {
            return (
                <li className="col-2 col-lg-2 one-photographer list-inline-item" key={k}>
                    <div className="child">
                        <a key={k} href={this.hrefFunc(photographer.number)}>
                            <img
                                alt={photographer.number}
                                width={photoSize[0]}
                                src={this.srcFunc(photographer.number)}
                            />
                        </a>
                        <p>{photographer.name ? photographer.name : "No Name"}</p>
                    </div>
                </li>
            );
        });
    }

    searchQueryChanged(oldQuery, newQuery) {
        // update as we add more queries
        return oldQuery.name !== newQuery.name;
    }

    handleScroll(e) {
        // doing some arithmetic with the scroll height here to detect when the user reaches the bottom of the list
        const bottom =
            Math.trunc((e.target.scrollHeight - e.target.clientHeight) / 10) <=
            Math.trunc(e.target.scrollTop / 10);

        // if we reach bottom we load the next page of photographers
        if (bottom) {
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
        if (this.searchQueryChanged(prevState.searchQueries, this.state.searchQueries)) {
            this.resetPaginationParameters();
            this.refetchPhotographers();
        }
        if (this.searchQueryChanged(prevState.searchQueries, this.state.searchQueries)) {
            this.resetPaginationParameters();
            this.refetchPhotographers();
        }
        if (prevState.activeDropdown !== this.state.activeDropdown) {
            let overlay = document.getElementById("overlay");
            if (this.state.activeDropdown) {
                overlay.classList.add("show");
                overlay.classList.remove("hide");
            } else {
                overlay.classList.add("hide");
                overlay.classList.remove("show");
            }
        }
    }

    render() {
        return (
            <div className="photographerList-container">
                <div id="overlay"></div>

                <div id={"banner"}>
                    <div className="header">
                        <div className="red-blue-box">
                            <RedBlueBox />
                        </div>
                        <p className="heading">Photographers</p>
                    </div>
                    <form className={"filterContainer"}>
                        <input
                            type="text"
                            id="photographerList-search"
                            placeholder="Search by name"
                            onChange={(e) => {
                                this.setState({ searchQueries: { name: e.target.value } });
                            }}
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
                                    />
                                    <DropDown
                                        id="sq-filter"
                                        blue={true}
                                        items={this.state.dropdownSearchOptions.squares}
                                        placeholder={"Map Square"}
                                        activeDropdown={this.state.activeDropdown}
                                        toggleActiveDropdown={this.toggleActiveDropdown}
                                    />
                                    <DropDown
                                        id="alph-filter"
                                        blue={true}
                                        items={this.state.dropdownSearchOptions.nameStartWith}
                                        placeholder={"Alphabet"}
                                        activeDropdown={this.state.activeDropdown}
                                        toggleActiveDropdown={this.toggleActiveDropdown}
                                    />
                                </div>
                            </div>
                            <div className="sortBy-container">
                                <p>Sort by:</p>
                                <DropDown
                                    id="sort"
                                    blue={false}
                                    items={this.state.dropdownSearchOptions.orderBy}
                                    placeholder={"---"}
                                    activeDropdown={this.state.activeDropdown}
                                    toggleActiveDropdown={this.toggleActiveDropdown}
                                />
                            </div>
                        </div>
                    </form>
                </div>

                <div className="photographerGallery">
                    <ul className="list-inline" onScroll={this.handleScroll}>
                        {this.getPhotoList()}
                        <div>{this.state.isLastPage ? "End of Results!!!" : "Loading..."}</div>
                    </ul>
                </div>
                <div>
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
};
