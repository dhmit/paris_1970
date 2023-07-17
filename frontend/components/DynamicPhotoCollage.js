
import React, { useEffect, useState } from "react";
import { Gallery } from "react-grid-gallery";

export default function DynamicPhotoCollage() {
    const [collageImages, setCollageImages] = useState([]);
    
    const GALLERY_HEIGHT = (window.screen.height * window.devicePixelRatio) / 9;
    let imgWidth = window.screen.width;
    let imgHeight = window.screen.height;
    const pixelRatio = window.devicePixelRatio;

    if (window.matchMedia("(min-width: 769px)").matches) {
        imgWidth = (imgWidth * pixelRatio) / 1;
        imgHeight = (imgHeight * pixelRatio) / 1.5;
    } else if (window.matchMedia("(min-width: 481px)").matches) {
        imgWidth = (imgWidth * pixelRatio) / 3.5;
        imgHeight = (imgHeight * pixelRatio) / 1;
    } else if (window.matchMedia("(min-width: 320px)").matches) {
        imgWidth = (imgWidth * pixelRatio) / 4;
        imgHeight = (imgHeight * pixelRatio) / 9;
    }
    
    useEffect(() => {
        const fetchData = async () => {
            const collageResponse = await fetch('/api/random_photos');
            const collageImg = await collageResponse.json();
            const collageImgDicts = collageImg.map(img => ({
                src:    img["photo_url"],
                url:    img['photo_page_url'],
                width:  imgWidth,
                height: imgHeight,
            }));
            setCollageImages(collageImgDicts);
        };
        fetchData();
    }, []);

    const handleClick = (index) => {
        const url = collageImages[index].url;
        window.open(url,'_self');
    };

    return (
        <div>
            <Gallery rowHeight={GALLERY_HEIGHT} margin={0} maxRows={3} images={collageImages} onClick={handleClick}/>
        </div>
    );
}

