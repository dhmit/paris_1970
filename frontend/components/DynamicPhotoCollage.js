import React from "react";
import {Gallery} from "react-grid-gallery";

// images
import Map_Page from "../images/featured/map page.png";
import Walking_Man from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_078.jpg";
import Car from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_008.jpg";
import Staring_Man from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_024.jpg";
import Roof from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_002.jpg";
import Neighbourhood from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_012.jpg";
import House from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_030.jpg";


const COLLAGE_IMAGES = [
    Map_Page,
    Walking_Man,
    Car,
    Staring_Man,
    Roof,
    Neighbourhood,
    House,
    "https://c2.staticflickr.com/9/8356/28897120681_3b2c0f43e0_b.jpg",
    "https://c4.staticflickr.com/9/8887/28897124891_98c4fdd82b_b.jpg",
    "https://c7.staticflickr.com/9/8546/28354329294_bb45ba31fa_b.jpg",
    "https://c6.staticflickr.com/9/8890/28897154101_a8f55be225_b.jpg",
];

export default function DynamicPhotoCollage() {
    const GALLERY_HEIGHT = (window.screen.height*pixelRatio)/9;

    let imgWidth = window.screen.width;
    let imgHeight = window.screen.height;
    const pixelRatio = pixelRatio;
    if (window.matchMedia("(min-width: 769px)").matches) {
        // laptops
        imgWidth  *= pixelRatio / 1;
        imgHeight *= pixelRatio / 1.5;
    } else if (window.matchMedia("(min-width: 481px)").matches) {
        // tablets
        imgWidth  *= pixelRatio / 3.5;
        imgHeight *= pixelRatio / 1;
    } else if (window.matchMedia("(min-width: 320px)").matches) {
        // phones
        imgWidth  *= pixelRatio / 4;
        imgHeight *= pixelRatio / 9;
    }

    const imgToImgDict = src => { return {src, width: imgWidth, height: imgHeight}; };
    const collageImgDicts = COLLAGE_IMAGES.map(src => imgToImgDict(src));

    return (
        <div>
            <Gallery rowHeight={GALLERY_HEIGHT} margin={0} maxRows={3} images={collageImgDicts} />
        </div>
    );
}
