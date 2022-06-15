import React from "react";
import NavBar from "../components/Navbar";
import Loading from "../components/Loading";
import Footer from "../components/Footer";

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
