import React from "react";
import Footer from "../../components/Footer";
import * as PropTypes from "prop-types";
import {debounce} from "../../common";

export class PhotographerListView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            photographers: [],
        };
    }

    hrefFunc(number) {
        return `/photographer/${number}`;
    }

    srcFunc(number) {
        return `${this.props.photoListDir}/${number}_photo.jpg`;
    }

    updatePhotographers(name) {
        debounce(async () => {
            const fetchedPhotographers = await this.fetchPhotographers(name);
            this.setState({photographers: fetchedPhotographers});
        }, 300)();
    }

    async fetchPhotographers(sq) {
        try {
            const res = await fetch(`/api/search_photographers?name=${sq}`);
            return res.json();
        } catch {
            return [];
        }
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

    componentDidMount() {
        this.updatePhotographers("");
    }

    render() {
        return (
            <>
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
                    Search By Name:{" "}
                    <input
                        onChange={(e) => {
                            this.updatePhotographers(e.target.value);
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
