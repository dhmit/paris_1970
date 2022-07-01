import React from "react";
import * as PropTypes from "prop-types";
import Legend from "./Legend";

export class Logo extends React.Component {
    constructor(props) {
        super(props);

        this.top = props.top;
        this.left = props.left;
        this.position_type = props.position;

    }

    render() {
        return (
            <div className="parent-bounding-box" style={{top: this.top+"%",
                                                         left: this.left+"%",
                                                         position:this.position_type}}>
                <div className="bottom-right-red-rectangle"/>
                <div className="top-left-blue-rectangle"/>
            </div>
        );
    }
}

Logo.propTypes = {
    top: PropTypes.number,
    left: PropTypes.number,
    position: PropTypes.string
};

Logo.defaultProps = {
    top: 0,
    left: 0,
    position: "relative"
};

export default Logo;


