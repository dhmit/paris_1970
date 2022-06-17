import React from "react";

const navbarLinks = [
    {
        name: "Search",
        link: "/search/"
    },
    {
        name: "Analyses",
        link: "/all_analysis/"
    },
    {
        name: "Similarities",
        link: "/similarity/"
    },
    {
        name: "About",
        link: "/about/"
    }
];

export class Navbar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            showNav: false
        };
    }

    render() {
        const show = (this.state.showNav) ? "show" : "";
        return (
            <div>
                <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                    <div className="container-fluid">
                        <a className="navbar-brand" style={{"fontSize": "200%"}}
                           href="/"><b>This Was Paris in 1970</b></a>
                        <button className="navbar-toggler" type="button"
                                onClick={() => {
                                    this.setState({showNav: !this.state.showNav});
                                }}
                                data-bs-toggle="collapse" data-bs-target="#navbarNav"
                                aria-controls="navbarNav" aria-expanded="false"
                                aria-label="Toggle navigation">
                            <span className="navbar-toggler-icon"></span>
                        </button>
                        <div className={"collapse navbar-collapse " + show} id="navbarNav">
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

export default Navbar;
