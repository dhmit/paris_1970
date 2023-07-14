import React, { useEffect,useState } from "react";
import {Gallery} from "react-grid-gallery";


export default function DynamicPhotoCollage() {
    const [collageImages, setCollageImages] = useState([]);

    useEffect(async ()=>{
      const collageResponse = await fetch('/api/random_photos');
      const collageImg = await collageResponse.json();
      setCollageImages(collageImg);
    }, []);

    const GALLERY_HEIGHT = (window.screen.height*window.devicePixelRatio)/9;

    let imgWidth = window.screen.width;
    let imgHeight = window.screen.height;
    const pixelRatio = window.devicePixelRatio;
    if (window.matchMedia("(min-width: 769px)").matches) {
        // laptops
        imgWidth = (imgWidth*pixelRatio)/1;
        imgHeight = (imgHeight*pixelRatio)/1.5;
        
    } else if (window.matchMedia("(min-width: 481px)").matches) {
        // tablets
        imgWidth = (imgWidth*pixelRatio)/3.5;
        imgHeight = (imgHeight*pixelRatio)/1;

    } else if (window.matchMedia("(min-width: 320px)").matches) {
        // phones
        imgWidth = (imgWidth*pixelRatio)/4;
        imgHeight = (imgHeight*pixelRatio)/9;
    }
    
    const collageImgDicts = [];
    collageImages?.forEach(img => {
       
        collageImgDicts.push({
          src : img["photo_url"],
          url : img['photo_page_url'],
          width: imgWidth,
          height: imgHeight,
        });  
    });
    
  const handleClick = (index) => {
    const url = collageImgDicts[index].url;
    window.open(url,'_self');
  };

    console.log(collageImgDicts);
    return (
        <div>
            <Gallery rowHeight={GALLERY_HEIGHT} margin={0} maxRows={3} images={collageImgDicts} onClick={handleClick}/>
        </div>
    );
}
