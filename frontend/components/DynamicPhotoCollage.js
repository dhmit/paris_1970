
import React ,{ useState } from "react";
import { Gallery } from "react-grid-gallery";
import { images as IMAGES } from "./collagephotos";

export default function DynamicPhotoCollage() {
  const height = (window.screen.height*window.devicePixelRatio)/9;
  const [images, setImages] = useState(IMAGES);
  
  return (
    <div>
      <Gallery rowHeight={height} margin={0} maxRows={3} images={images} />
    </div>
  );
}
