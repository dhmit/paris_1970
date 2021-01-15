/**
 *  Components that are reused frequently throughout the project
 */

import React, { Component } from 'react';
import * as PropTypes from 'prop-types';
import * as d3 from 'd3';

/**
 * Component used to render paths into SVGs
 */
export class MapPath extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            fill: this.props.fill,
        };
        this.pathRef = React.createRef();
    }

    componentDidUpdate(prevProps) {
        /**
         *  Explanation of d3 transition in React:
         *  - Since constructor is only called when a component is created, this.state.fill
         *  will be set to the initial color
         *  - When the year changes, MapPath gets new props from this.props. However,
         *  this.state.fill is still the previous color because the constructor is only called once
         *  - Use d3 to select this MapPath element and apply transition
         *  - Once the transition is over, set this.state.fill to the new color
         */

        if (prevProps.fill !== this.props.fill) {
            if (this.props.useColorTransition) {
                d3.select(this.pathRef.current)
                    .transition()
                    .duration(500)
                    .attr('fill', () => {
                        return this.props.fill;
                    })
                    .on('end', () => {
                        this.setState({ fill: this.props.fill });
                    });
            } else {
                this.setState({ fill: this.props.fill });
            }
        }
    }

    render() {
        return (
            <path
                d={this.props.path}
                stroke={this.props.stroke}
                strokeWidth={this.props.strokeWidth}
                fill={this.state.fill}
                id={this.props.id}
                onMouseOver={this.props.handleCountryMouseover}
                onClick={this.props.handleCountryClick}
                ref={this.pathRef}
            />
        );
    }
}
MapPath.propTypes = {
    path: PropTypes.string,
    id: PropTypes.string,
    fill: PropTypes.string,
    handleCountryMouseover: PropTypes.func,
    handleCountryClick: PropTypes.func,
    stroke: PropTypes.string,
    strokeWidth: PropTypes.string,
    useColorTransition: PropTypes.bool,
};


export class CaptionedImage extends React.Component {
    render() {
        return (
            <figure className="figure w-100">
                <img
                    className='figure-img img-fluid w-100'
                    src={'/static/img/' + this.props.filename}
                    alt={this.props.alt}
                />
                <figcaption className="figure-caption" style={ { textAlign: 'left' } }>
                    {this.props.caption}
                </figcaption>
            </figure>

        );
    }
}
CaptionedImage.propTypes = {
    filename: PropTypes.string,
    caption: PropTypes.object,
    alt: PropTypes.string,
};

export class Loading extends React.Component {
    render() {
        return (
            <div className="m-auto">
                <div className="spinner-border" role="status">
                    <span className="sr-only">Loading...</span>
                </div>
            </div>
        );
    }
}

export class Footer extends React.Component {
    render() {
        return (
            <footer className="footer bg-white text-dark text-center mt-auto">
                <div className="container-fluid">
                    <div className="row">
                        <div className="col-4 py-3">
                            <a href="https://digitalhumanities.mit.edu/">
                                <img
                                    src="/static/img/footer/dh_logo.svg"
                                    className='footer-img'
                                    alt='Digital Humanities at MIT Logo'
                                />
                            </a>
                        </div>
                        <div className="col-4 py-3">
                            <a href="https://www.mit.edu/">
                                <img
                                    src="/static/img/footer/mit_logo.svg"
                                    className='footer-img'
                                    alt='MIT Logo'
                                />
                            </a>
                        </div>
                        <div className="col-4 py-3">
                            <a href="https://www.mellon.org/">
                                <img
                                    src="/static/img/footer/mellon_logo.svg"
                                    className='footer-img'
                                    alt="Mellon Foundation Logo"
                                />
                            </a>
                        </div>
                    </div>
                </div>
            </footer>
        );
    }
}

const navbarLinks = [
    { name: 'Search', link: '/search/' },
    { name: 'Analyses', link: '/all_analysis/' },
    { name: 'Similarities', link: '/similarity/' },
    { name: 'About', link: '/about/' },
];

export class Navbar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            showNav: false,
        };
    }

    render() {
        const show = (this.state.showNav) ? 'show' : '';
        return (
            <div>
                <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                    <div className="container-fluid">
                        <a className="navbar-brand" style={{ 'font-size': '200%' }}
                            href="/"><b>This Was Paris in 1970</b></a>
                        <button className="navbar-toggler" type="button"
                            onClick={() => { this.setState({ showNav: !this.state.showNav }); }}
                            data-bs-toggle="collapse" data-bs-target="#navbarNav"
                            aria-controls="navbarNav" aria-expanded="false"
                            aria-label="Toggle navigation">
                            <span className="navbar-toggler-icon"></span>
                        </button>
                        <div className={'collapse navbar-collapse ' + show} id="navbarNav">
                            <ul className="navbar-nav ml-auto">
                                {
                                    navbarLinks.map((page) => (
                                        <li key={page.name} className="nav-item">
                                            <a key={page.name} className="nav-link"
                                                href={page.link}>{page.name}</a>
                                        </li>
                                    ))
                                }
                            </ul>
                        </div>
                    </div>
                </nav>
            </div>
        );
    }
}

export class LoadingPage extends React.Component {
    render() {
        return (
            <>
                <Navbar />
                <Loading/>
                <Footer />
            </>
        );
    }
}
