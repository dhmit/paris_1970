import React from "react";
import * as PropTypes from "prop-types";

export class CaptionedImage extends React.Component {
    render() {
        return (
            <figure className="figure w-100">
                <img
                    className="figure-img img-fluid w-100"
                    src={"/static/img/" + this.props.filename}
                    alt={this.props.alt}
                />
                <figcaption className="figure-caption" style={{textAlign: "left"}}>
                    {this.props.caption}
                </figcaption>
            </figure>

        );
    }
}

CaptionedImage.propTypes = {
    filename: PropTypes.string,
    caption: PropTypes.object,
    alt: PropTypes.string
};


export default CaptionedImage;
