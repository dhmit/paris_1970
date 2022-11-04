import { Image } from "react-grid-gallery";

// images
import Map_Page from "../images/featured/map page.png";
import Walking_Man from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_078.jpg";
import Car from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_008.jpg";
import Staring_Man from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_024.jpg";
import Roof from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_002.jpg";
import Neighbourhood from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_012.jpg";
import House from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_030.jpg";

import photo_1 from "../images/featured/BHVP_PH_CetaitParis_DP_0031_01_002.jpg";
import photo_2 from "../images/featured/BHVP_PH_CetaitParis_DP_0031_01"


if (window.matchMedia('(min-width: 769px)').matches) {
    // screens like laptops
    var width = (window.screen.width*window.devicePixelRatio)/1;
	var height = (window.screen.height*window.devicePixelRatio)/1.5;
} else if (window.matchMedia('(min-width: 481px)').matches){
    // screens like tablets
    var width = (window.screen.width*window.devicePixelRatio)/3.5;
	var height = (window.screen.height*window.devicePixelRatio)/1;
	
}else if (window.matchMedia('(min-width: 320px)').matches){
    // phone screens
    var width = (window.screen.width*window.devicePixelRatio)/4;
	var height = (window.screen.height*window.devicePixelRatio)/9;
}



// const width = (window.screen.width*window.devicePixelRatio)/4;
// const height = (window.screen.height*window.devicePixelRatio)/6;

export const images = [
   [ {
        src : Map_Page,
        width:width,
        height:height,

    },
    {
        src : Walking_Man,
        width:width,
        height:height,

    },
    {
        src : Car,
        width:width,
        height:height,

    },
    {
        src : Staring_Man,
        width:width,
        height:height,

    },
    {
        src : Roof,
        width:width,
        height:height,

    },
    {
        src : Neighbourhood,
        width:width,
        height:height,

    },
    {
        src : House,
        width:width,
        height:height,

    },
    {
        src: "https://c2.staticflickr.com/9/8356/28897120681_3b2c0f43e0_b.jpg",
        width: width,
        height: height,
    },
    {
        src: "https://c4.staticflickr.com/9/8887/28897124891_98c4fdd82b_b.jpg",
        width: width,
        height: height,

    },
    {
        src: "https://c7.staticflickr.com/9/8546/28354329294_bb45ba31fa_b.jpg",
        width: width,
        height: height,
    },
    {
        src: "https://c6.staticflickr.com/9/8890/28897154101_a8f55be225_b.jpg",
        width: width,
        height: height,
    
      },],

];