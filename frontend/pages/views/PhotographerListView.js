import React from "react";
import Footer from "../../components/Footer";
import * as PropTypes from "prop-types";
import { debounce } from "../../common";

import Chevron from "../../images/icons/chevron_down.svg";
import RedBlueBox from "../../images/icons/red_blue_box.svg";

class DropDown extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selected: null,
        };
    }

    render() {
        return (
            <div
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
        };
        this.refetchPhotographers = this.refetchPhotographers.bind(this);
        this.resetPaginationParameters = this.resetPaginationParameters.bind(this);
        this.handleScroll = this.handleScroll.bind(this);

        // THIS IS DUMMY DATA
        this.LOCATIONS = ["1", "2", "3"];
        this.SQUARES = ["4", "5", "6"];
        this.ALPHABET = ["7", "8", "9"];
        this.SORTS = ["10", "11", "12"];
    }

    hrefFunc(number) {
        return `/photographer/${number}`;
    }

    srcFunc(number) {
        return `${this.props.photoListDir}/${number}_photo.jpg`;
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

    handleScroll = () => {
        // Detecting scroll end adapted from https://stackoverflow.com/a/4620986
        if (this.scrollOverTimer !== null) {
            clearTimeout(this.scrollOverTimer);
        }

        let dropdowns = document.getElementsByClassName("dropdown-items");
        for (const elt of dropdowns) {
            elt.classList.add("d-none");
        }

        let banner = document.getElementById("banner");

        this.scrollOverTimer = setTimeout(() => {
            banner.classList.add("grow");
            banner.classList.remove("shrink");
        }, 1000);

        banner.classList.add("shrink");
        banner.classList.remove("grow");

        if (window.scrollY > 70) {
            banner.style.position = "fixed";
            banner.style.top = "0px";
        } else {
            banner.style.position = "absolute";
            banner.style.top = "70px";
        }
    };

    toggleActiveDropdown = (dropDown) => {
        this.setState({ activeDropdown: dropDown });
    };

    componentDidMount() {
        this.refetchPhotographers();
        window.addEventListener("scroll", this.handleScroll);
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

    componentWillUnmount() {
        window.removeEventListener("scroll", this.handleScroll);
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
                                        items={this.LOCATIONS}
                                        placeholder={"Locations"}
                                        activeDropdown={this.state.activeDropdown}
                                        toggleActiveDropdown={this.toggleActiveDropdown}
                                    />
                                    <DropDown
                                        id="sq-filter"
                                        blue={true}
                                        items={this.SQUARES}
                                        placeholder={"Map Square"}
                                        activeDropdown={this.state.activeDropdown}
                                        toggleActiveDropdown={this.toggleActiveDropdown}
                                    />
                                    <DropDown
                                        id="alph-filter"
                                        blue={true}
                                        items={this.ALPHABET}
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
                                    items={this.SORTS}
                                    placeholder={"---"}
                                    activeDropdown={this.state.activeDropdown}
                                    toggleActiveDropdown={this.toggleActiveDropdown}
                                />
                            </div>
                        </div>
                    </form>
                </div>

                <div className="photographerGallery">
                    <ul
                        className="list-inline"
                        style={{
                            overflowY: "scroll",
                            maxHeight: "700px",
                            width: "99%",
                        }}
                        onScroll={this.handleScroll}
                    >
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
