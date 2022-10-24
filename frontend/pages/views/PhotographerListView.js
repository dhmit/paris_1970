import React from "react";
import Footer from "../../components/Footer";
import * as PropTypes from "prop-types";


import Chevron from "../../images/icons/chevron_down.svg";

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
                    className="dropdown-select"
                    style={{
                        border: this.props.blue
                            ? "1px solid $color-turquoise"
                            : "1px solid #FB2F2A",
                    }}
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
            photographers: JSON.parse(this.props.photographers),
            timer: null,
            activeDropdown: null,
        };

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

    getPhotoList() {
        const photoSize = [100, 100];
        return this.state.photographers.map((photog, k) => {
            return (
                <li className="col-2 col-lg-2 one-photographer list-inline-item" key={k}>
                    <div className="child">
                        <a key={k} href={this.hrefFunc(photog.number)}>
                            <img
                                alt={photog.number}
                                width={photoSize[0]}
                                src={this.srcFunc(photog.number)}
                            />
                        </a>
                        <p>{photog.name ? photog.name : "No Name"}</p>
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

        this.scrollOverTimer = setTimeout(() => {
            // If the timer elapses, show to
            // this.setState({retract:true});
            document.getElementsByClassName("banner")[0].classList.add("grow");
            document.getElementsByClassName("banner")[0].classList.remove("shrink");
        }, 1000);

        document.getElementsByClassName("banner")[0].classList.add("shrink");
        document.getElementsByClassName("banner")[0].classList.remove("grow");

        if (window.scrollY > 70) {
            document.getElementsByClassName("banner")[0].style.position = "fixed";
            document.getElementsByClassName("banner")[0].style.top = "0px";
        } else {
            document.getElementsByClassName("banner")[0].style.position = "absolute";
            document.getElementsByClassName("banner")[0].style.top = "70px";
        }
    };

    toggleActiveDropdown = (dropDown) => {
        this.setState({activeDropdown: dropDown});
    };

    componentDidMount() {
        // if (!this.galleryRef) {
        //     return;
        //   }
        window.addEventListener("scroll", this.handleScroll);
    }

    componentDidUpdate(prevState) {
        console.log(this.state.activeDropdown);

        if (prevState.activeDropdown !== this.state.activeDropdown) {
            if (this.state.activeDropdown) {
                document.getElementsByClassName("overlay")[0].classList.add("show");
                document.getElementsByClassName("overlay")[0].classList.remove("hide");
            } else {
                document.getElementsByClassName("overlay")[0].classList.add("hide");
                document.getElementsByClassName("overlay")[0].classList.remove("show");
            }
        }
    }

    componentWillUnmount() {
        window.removeEventListener("scroll", this.handleScroll);
    }

    render() {
        return (
            <>
                <div className="photographerList-container">
                    <div className="overlay"></div>

                    <div className={"banner"}>
                        <p className="heading">Photographers</p>
                        <form className={"filterContainer"}>
                            {/* TODO: add magnify glass icon down */}
                            <input
                                type="text"
                                id="photographerList-search"
                                placeholder="Search by name"
                            />
                            <div className="advancedSearch-container">
                                <div className="filterBy-container">
                                    <p>Filter by:</p>
                                    <div
                                        style={{
                                            display: "flex",
                                            flexDirection: "row",
                                            columnGap: "5vw",
                                        }}
                                    >
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
                        {/* <ul className="list-inline">{this.getPhotoList()}</ul> */}
                    </div>
                </div>

                <div>
                    <Footer />
                </div>
            </>
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
