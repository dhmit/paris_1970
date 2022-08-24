import React from "react";
import Footer from "../../components/Footer";
import * as PropTypes from "prop-types";


export class PhotographerListView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            photographers: JSON.parse(this.props.photographers)
        };
    }

    hrefFunc(number) {
        return `/photographer/${number}`;
    };

    srcFunc(number) {
        return `${this.props.photoListDir}/${number}_photo.jpg`;
    };

    getPhotoList() {
        const photoSize = [100, 100];
        return this.state.photographers.map((photog, k) => {
            return (
                <li className="col-2 col-lg-2 one-photographer list-inline-item" key={k}>
                    <div className="child">
                        <a key={k}
                           href={this.hrefFunc(photog.number)}>
                            <img
                                alt={photog.number}
                                width={photoSize[0]}
                                src={this.srcFunc(photog.number)}/>
                        </a>
                        <p>{photog.name ? photog.name : "No Name"}</p>
                    </div>
                </li>
            );
        });

    }

    render() {
        return (
            <>
                <div className="row">
                    <p style={{
                        fontSize: "30px",
                        fontWeight: "600"
                    }}>Photographers</p>
                </div>
                <div className="row">
                    <ul className="list-inline">{this.getPhotoList()}</ul>
                </div>
                <div>
                    <Footer/>
                </div>
            </>
        );
    }
}


PhotographerListView.propTypes = {
    photoListDir: PropTypes.string,
    photographers: PropTypes.string
};

