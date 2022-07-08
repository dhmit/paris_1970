import React from "react";
import Loading from "../components/Loading";
import Footer from "../components/Footer";

export class LoadingPage extends React.Component {
    render() {
        return (
            <>
                <Loading/>
                <Footer/>
            </>
        );
    }
}

export default LoadingPage;
