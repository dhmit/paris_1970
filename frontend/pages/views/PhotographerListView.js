import React from "react";
import Footer from "../../components/Footer";
import * as PropTypes from "prop-types";
import { debounce } from "../../common";

export class PhotographerListView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            searchQueries: { name: "" },
            photographers: [],
            pageNumber: 0,
            isLastPage: false,
        };
    }

    hrefFunc(number) {
        return `/photographer/${number}`;
    }

    srcFunc(number) {
        return `${this.props.photoListDir}/${number}_photo.jpg`;
    }

    refetchPhotographers() {
        const fetchPhotographers = async (sq) => {
            const newPageNumber = this.state.pageNumber + 1;
            try {
                console.log("Fetching.....");
                const res = await fetch(
                    `/api/search_photographers?name=${sq}&page=${newPageNumber}`
                );
                return res.json();
            } catch {
                return [];
            }
        };
        debounce(async () => {
            const { results, is_last_page, page_number } = await fetchPhotographers(
                this.state.searchQueries.name
            );
            this.setState({
                photographers: this.state.photographers.concat(results),
                isLastPage: is_last_page,
                pageNumber: parseInt(page_number),
            });
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

    resetPaginationParameters() {
        this.setState({ pageNumber: 0, isLastPage: false, photographers: [] });
    }

    componentDidMount() {
        this.refetchPhotographers();
    }

    render() {
        return (
            <>
                <button onClick={this.refetchPhotographers}>Nextpage</button>
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
                            this.setState({ searchQueries: { name: e.target.value } });
                        }}
                    />
                </div>
                <div className="row">
                    <ul className="list-inline">{this.getPhotoList()}</ul>
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
