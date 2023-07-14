import React from "react";
import HomeSections from "../components/HomeSections";
import Logo_Gif from "../images/gif/rec-animation-english---Copy.gif";
import Car from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_008.jpg";
import Arrows from "../images/icons/scroll_down.svg";
import Collage from "../components/DynamicPhotoCollage";
import { StrictMode } from "react";


export class HomePage extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <section>
                
                <div className="main-section">
                    <img src={Logo_Gif} alt="Paris Logo"/>
                    <img src={Car} className="background" alt="Background image: Car"/>
                </div>
                <div className = "see_below_text"> Scroll down to enter</div>
                <div className = "scroll_down">
                    <a className = "btn transparent_button" href="#home-sections"><Arrows/></a>
                </div>
                <HomeSections/>
            </section>
        );
    }
}
