import React from "react";
import * as PropTypes from "prop-types";
import PhotoViewer from "../../components/PhotoViewer";


export class MapSquareContent extends PhotoViewer {
    constructor(props) {
        super(props);
    }

    render() {
        return (<>
            {this.props.photos.length

                ? (<>
                    <h6 className={"text-uppercase"}>Example photos</h6>
                    <ul className={"list-inline"}>{
                        this.getPhotoGrid(this.props.photos, {
                            "photoSize": [120, 120],
                            "className": "example-photo"
                        })
                    }
                    </ul>
                    <a className={"link"}
                       href={"/map_square/" + this.props.mapSquare}>
                        Go to map square
                    </a>
                </>)
                : <></>
            }
            {this.props.photographers.length ? <>
                <h6 className={"text-uppercase"}>Photographers</h6>
            </> : <></>}
        </>);
    }
}

MapSquareContent.propTypes = {
    mapSquare: PropTypes.number,
    photos: PropTypes.array,
    photographers: PropTypes.array,
    photoDir: PropTypes.string
};

export default MapSquareContent;
