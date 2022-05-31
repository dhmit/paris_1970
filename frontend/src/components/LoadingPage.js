import React from "react";
import NavBar from "./Navbar";
import Loading from "./Loading";
import Footer from "./Footer";

export class LoadingPage extends React.Component {
    render() {
        return (
            <>
                <NavBar/>
                <Loading/>
                <Footer/>
            </>
        );
    }
}

export default LoadingPage;
