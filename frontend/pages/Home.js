import React from "react";
import Sections from "../components/Sections";
import "../scss/animation.scss";

// animation
import Logo_Gif from "../images/gif/rec-animation-english---Copy.gif";
import Car from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_008.jpg";
import Logo from "../images/featured/nav-logo.png";


export class HomePage extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {

        return (
            <div>
                <div className="animation" style={{backgroundImage: `url(${Logo_Gif})`}}>
                    <img src={Car} className="background"/>

                </div>


                <Sections/>
            </div>
        );
    }
}
