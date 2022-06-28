import React from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";


class Sign_In extends React.Component {
    render() {
        //return (<><p>bup</p></>);
        return (<>
            <Navbar/>
            <div className="page">
                <div className="sign-in-title">
                    Sign In
                </div>
                <form action="/signintest/" method="post">
                    <label /*htmlFor="user"*/>Username:</label>
                    <br></br>
                    <input type="text" id="user" name="user"></input>
                    <br></br>
                    <label /*htmlFor="lname"*/>Password:</label>
                    <br></br>
                    <input type="password" id="pass" name="pass"></input>
                    <br></br>
                    <input type="submit" value="Log In"></input>
                </form>
            </div>
            <Footer/>
        </>);
    }
}

export default Sign_In;
