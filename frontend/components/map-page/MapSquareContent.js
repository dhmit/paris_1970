import React from "react";
import * as PropTypes from "prop-types";

function MapSquareContent(props) {

    return <>
        <p>{props.mapSquare}</p>
    </>;
}

MapSquareContent.propTypes = {
    mapSquare: PropTypes.number,
    photos: PropTypes.array,
    photographers: PropTypes.array
};

export default MapSquareContent;
