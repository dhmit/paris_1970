import React from "react";
import * as PropTypes from "prop-types";

export const SIDES = {
    CLEANED: "cleaned",
    FRONT: "front",
    BACK: "back"
};

function getValue(dictionary, key, default_val) {
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

    getSource (photoData, displaySide = false) {
        photoData.propTypes = {
            map_square_number: PropTypes.object
        };
        if (!displaySide) {
            const availableSides = Object.values(SIDES)
            .filter(
                (side) => photoData[`${side}_src`]
            );
            displaySide = availableSides.length > 0 ? availableSides[0] : "";
        }
        return `${this.props.photoDir}/${photoData.map_square_number}/${photoData.number}_${displaySide}.jpg`;
    };

    getPhotoGrid (photoData, config={}) {
        const className = getValue(config, "className", "");
        const photoSize = getValue(config, "photoSize", [100, 100]);
        const titleFunc = getValue(
            config,
            "titleFunc",
            (k, photo) => `Map Square: ${photo["map_square_number"]}` +
                                        `, Photo: ${photo["number"]}`
        );
        const hrefFunc = getValue(
            config,
            "hrefFunc",
            (k, photo) => `/photo/${photo["map_square_number"]}/${photo["number"]}/`
        );
        return photoData.map((photo, k) => {
            photo.propTypes = {
                cleaned_src: PropTypes.bool,
                front_src: PropTypes.bool
            };
            if (photo.front_src || photo.cleaned_src) {
                return (
                    <a
                        key={k}
                        className={className}
                        title={titleFunc(k, photo)}
                        href={hrefFunc(k, photo)}>
                        <img
                            alt={photo.alt}
                            width={photoSize[0]}
                            height={photoSize[1]}
                            src={this.getSource(photo)}
                        />
                    </a>
                );
            }
            return "";
        });
    }
}

PhotoViewer.propTypes = {
    photoDir: PropTypes.string
};
