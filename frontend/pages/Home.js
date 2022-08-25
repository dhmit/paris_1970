import React from "react";
import HomeSections from "../components/HomeSections";
import Logo_Gif from "../images/gif/rec-animation-english---Copy.gif";
import Car from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_008.jpg";


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
                <HomeSections/>
            </section>
        );
    }
}
