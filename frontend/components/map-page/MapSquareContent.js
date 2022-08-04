import React from "react";
import * as PropTypes from "prop-types";

function MapSquareContent(props) {
    return <>
        <p>Hello there {props.mapSquare}</p>
    </>;
}

MapSquareContent.propTypes = {
    mapSquare: PropTypes.string
};

export default MapSquareContent;
