import React, { Component } from 'react';
import * as PropTypes from 'prop-types';

class Navbar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            showNav: false,
        };
    }

    render() {
        return (
            <div>
                <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                    <a className="navbar-brand" style={{ 'font-size': '200%' }}
                        href="/"><b>This Was Paris in 1970</b></a>
                    <button className="navbar-toggler" type="button" data-toggle="collapse"
                        data-target="#navbarNav" aria-controls="navbarNav"
                        aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <ul className="navbar-nav ml-auto">
                        <li className="collapse navbar-collapse" id="navbarNavAltMarkup">
                            <div className="navbar-nav">
                                <a className="nav-item nav-link"
                                    style={{ 'font-size': '150%', 'color': 'light-grey' }}
                                    href="/about">About</a>
                            </div>
                        </li>
                    </ul>
                </nav>
            </div>
        );
    }
}
Navbar.propTypes = {
    currentPage: PropTypes.string,
};

export default Navbar;
