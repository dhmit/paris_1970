import React from "react";
import Footer from "../../components/Footer";
import * as PropTypes from "prop-types";
import {debounce} from "../../common";

export class PhotographerListView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            searchQueries: {name: ""},
            photographers: [],
            pageNumber: 1,
            isLastPage: false,
        };
        this.refetchPhotographers = this.refetchPhotographers.bind(this);
        this.resetPaginationParameters = this.resetPaginationParameters.bind(this);
        this.handleScroll = this.handleScroll.bind(this);
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
                const {results, is_last_page, page_number} = await fetchPhotographers(
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

    componentDidUpdate(prevProps, prevState) {
        if (this.searchQueryChanged(prevState.searchQueries, this.state.searchQueries)) {
            this.resetPaginationParameters();
            this.refetchPhotographers();
        }
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
        this.setState({pageNumber: 0, isLastPage: false, photographers: []});
    }

    componentDidMount() {
        this.refetchPhotographers();
    }

    render() {
        return (
            <div className="photographers-container">
                <div className="row">
                    <p
                        style={{
                            fontSize: "30px",
                            fontWeight: "600",
                        }}
                    >
                        Photographers
                    </p>
                </div>
                <div>
                    Search By Name:&nbsp;
                    <input
                        onChange={(e) => {
                            this.setState({searchQueries: {name: e.target.value}});
                        }}
                    />
                </div>
                <div className="row">
                    <ul
                        className="list-inline"
                        style={{
                            overflowY: "scroll",
                            maxHeight: "700px",
                            width: "99%",
                        }}
                        onScroll={this.handleScroll}
                    >
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
