import React from "react";
import Footer from "../../components/Footer";
import * as PropTypes from "prop-types";
import {debounce} from "../../common";

import Chevron from "../../images/icons/chevron_down.svg";
import RedBlueBox from "../../images/icons/red_blue_box.svg";

class DropDown extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            toggleDropDown: false,
            selected: null,
        };
    }

    render() {
        return (
            <div
                className="dropdown-container"
                onMouseEnter={() => {
                    this.setState({toggleDropDown: true});
                    let dropdowns = document.getElementsByClassName("dropdown-items");
                    for (const elt of dropdowns) {
                        if (elt.id !== this.props.id) {
                            elt.classList.add("d-none");
                        }
                    }
                    this.props.toggleActiveDropdown(this.props.id);
                }}
                onMouseLeave={() => {
                    this.setState({toggleDropDown: false});
                    this.props.toggleActiveDropdown(null);
                }}
            >
                <div
                    className={`dropdown-select ${this.props.blue?"blue-border":"red-border"}`}
                >
                    <p>{this.state.selected || this.props.placeholder}</p>
                    <Chevron/>
                </div>
                <div
                    className={`dropdown-items ${this.state.toggleDropDown ? "" : "d-none"}`}
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
                                        this.setState({selected: item});
                                    } else {
                                        this.setState({selected: null});
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
            activeDropdown: null,
            photographers: [],
        };


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

    updatePhotographers(name) {
        const fetchPhotographers = async (sq) => {
            try {
                const res = await fetch(`/api/search_photographers?name=${sq}`);
                return res.json();
            } catch {
                return [];
            }
        };
        debounce(async () => {
            const fetchedPhotographers = await fetchPhotographers(name);
            this.setState({photographers: fetchedPhotographers});
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
        this.setState({activeDropdown: dropDown});
    };

    componentDidMount() {
        this.updatePhotographers("");
        window.addEventListener("scroll", this.handleScroll);
    }

    componentDidUpdate(prevState) {

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
                        <div className="red-blue-box"><RedBlueBox/></div>
                        <p className="heading">Photographers</p>
                        </div>
                        <form className={"filterContainer"}>
                            <input
                                type="text"
                                id="photographerList-search"
                                placeholder="Search by name"
                                onChange={(e) => {
                                    this.updatePhotographers(e.target.value);
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
                        <ul className="list-inline">{this.getPhotoList()}</ul>
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
