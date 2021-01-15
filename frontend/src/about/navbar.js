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
        const aboutClassName = (
            `about-nav-link ${this.props.currentPage === 'about' && 'font-weight-bold'}`
        );

        return (
            <nav>
                <div className='about-nav'>
                    <div className='d-sm-block d-none'>
                        <a className='nav-title' href='/'>
                            This was Paris in 1970
                        </a>
                    </div>
                    <div className='d-block d-sm-none'>
                        <a className='nav-title-small' href='/'>
                            This was Paris in 1970
                        </a>
                    </div>
                    <div className='d-none d-lg-block ml-auto'>
                        <a className={aboutClassName} href='/about/'>About</a>
                    </div>
                    <div
                        className="hamburger d-block d-lg-none"
                        onClick={() => { this.setState({ showNav: !this.state.showNav }); }}
                    >
                        <div className="rectangle"/>
                        <div className="rectangle"/>
                        <div className="rectangle"/>
                    </div>
                </div>
                {
                    this.state.showNav
                    && <div className='alternate-nav d-block d-lg-none'>
                        <a className='alternate-link' href='/about/'>About</a>
                    </div>
                }
            </nav>
        );
    }
}
Navbar.propTypes = {
    currentPage: PropTypes.string,
};

export default Navbar;
