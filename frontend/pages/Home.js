import React, { StrictMode } from "react";
import HomeSections from "../components/HomeSections";
import Logo_Gif from "../images/gif/rec-animation-english---Copy.gif";
import Car from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_008.jpg";
import Collage from '../components/DynamicPhotoCollage';


export class HomePage extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <StrictMode>
                <Collage/>
            </StrictMode>
   
            // <section>
            //     <div className="main-section">
            //         <img src={Logo_Gif} alt="Paris Logo"/>
            //         <img src={Car} className="background" alt="Background image: Car"/>
            //     </div>
                
            //     {/* <HomeSections/> */}
            // </section>
        );
    }
}
