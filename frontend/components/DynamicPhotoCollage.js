import React from "react";
import * as PropTypes from "prop-types";

export class DynamicPhotoCollage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            image_looping_queue: []
        };
    }

    async componentDidMount() {
        //Asynchronously load batches of photos and have loaded photos displayed at random time
        // intervals. There will be a limit to the amount of photos loaded, in which case the
        // photos randomly displayed will be looped.
    }

    render() {
        {
            //For a lg-up screens, display 9 images in a 3x3 grid, where each cell changes pictures.
        }
        return(<p>test</p>);
    }
}

DynamicPhotoCollage.propTypes = {
    images: PropTypes.object
};


export default DynamicPhotoCollage;
