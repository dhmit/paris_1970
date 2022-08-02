import React from "react";
import ParisMap from "../components/ParisMap";
import * as PropTypes from "prop-types";
import PhotoViewer from "../components/PhotoViewer";

class TagView extends PhotoViewer {
    constructor(props) {
        super(props);
    }

    render() {
        if (this.props.tagPhotos.length === 0) {
            return (<>
                Tag {this.props.tagName} is not in the database.
            </>);
        }
        const tag = this.props.tagName;
        const photos = JSON.parse(this.props.tagPhotos);

        return (<>
            <div className="row">
                <div className="tag-info col-12 col-lg-5">
                    <p className="tag-header">Photographs tagged</p>
                    <p className="tag-title">{tag}</p>
                    <>{this.getPhotoGrid(photos, {"photoSize": [120, 120]})}</>
                </div>
                <div className="tag-map col-12 col-lg-7">
                    <ParisMap
                        className="tags-map"
                        zoom={14}
                        layers={{}}
                    />
                </div>
            </div>
        </>);
    }
}

TagView.propTypes = {
    tagName: PropTypes.string,
    tagPhotos: PropTypes.string
};

export default TagView;
