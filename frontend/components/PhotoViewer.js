import React from "react";

export function getValue(dictionary, key, default_val) {
    let result = dictionary[key];
    if (typeof result === "undefined") {
        result = default_val;
    }
    return result;
}

export class PhotoViewer extends React.Component {
    constructor(props) {
        super(props);
    }

    getSource(photoData, displaySide = "photo") {
        if (displaySide === "photo") {
            return photoData.photo_url;
        } else {
            return photoData.slide_url;
        }
    }

    getPhotoGrid(photoData, config = {}) {
        const className = getValue(config, "className", "");
        const photoSize = getValue(config, "photoSize", [100, 100]);
        const titleFunc = getValue(
            config,
            "titleFunc",
            (_, photo) =>
                `Map Square: ${photo["map_square_number"]}` +
                `, Folder: ${photo.folder}, Photo: ${photo["number"]}`
        );

        const hrefFunc = getValue(
            config,
            "hrefFunc",
            (_, photo) => `/photo/${photo.map_square_number}/${photo.folder}/${photo.number}/`
        );

        const onClickFunc = getValue(config, "onClickFunc", (_k, _photo) => (_e) => {});
        return photoData.map((photo, k) => {
            return (
                <li
                    className={`default-photo photo-item-background text-center list-inline-item ${className}`}
                    key={k}
                    onClick={(e) => {
                        onClickFunc(k, photo)(e);
                        window.open(hrefFunc(k, photo), "_self");
                    }}
                    style={{
                        width: photoSize[0],
                        height: photoSize[1],
                        backgroundColor: "rgb(236, 243, 244)",
                    }}
                >
                    <a
                        className={className}
                        title={titleFunc(k, photo)}
                        href={hrefFunc(k, photo)}
                        onClick={onClickFunc(k, photo)}
                    >
                        <img
                            alt={photo.alt}
                            style={{
                                maxWidth: photoSize[0],
                                maxHeight: photoSize[1],
                            }}
                            src={this.getSource(photo)}
                        />
                    </a>
                </li>
            );
        });
    }

    getPhotoSlider(photoData, config = {}) {
        // TODO: Disable scroll buttons when there are no more photos to scroll through
        return (
            <div className="photos-box">
                <button
                    type="button"
                    className="slider-scroll-left btn-dark"
                    onClick={() =>
                        (document.getElementById("photo-slider").scrollLeft -=
                            document.getElementById("photo-slider").clientWidth)
                    }
                >
                    &#8249;
                </button>
                <ul id="photo-slider" className="slider-photos list-inline">
                    {this.getPhotoGrid(photoData, config)}
                </ul>
                <button
                    type="button"
                    className="slider-scroll-right btn-dark"
                    onClick={() =>
                        (document.getElementById("photo-slider").scrollLeft +=
                            document.getElementById("photo-slider").clientWidth)
                    }
                >
                    &#8250;
                </button>
            </div>
        );
    }
}

export default PhotoViewer;
