import React from "react";
import * as PropTypes from "prop-types";

export class TitleDecorator extends React.Component {
    constructor(props) {
        super(props);

        //Positions in terms of %
        this.top = props.top;
        this.left = props.left;
        //Position anchor (relative, absolute, etc)
        this.position_type = props.position;
        //For identifying css styling. Check titleDecorator.scss for valid inputs
        this.decorator_type = props.decorator_type;

    }

    render() {
        return (
            //All decorators can consist of a red square and/or a blue square. They are contained
            //within a parent div/bounding box
            <div className={"parent-bounding-box-" + this.decorator_type} style={{
                top: this.top + "%",
                left: this.left + "%",
                position: this.position_type
            }}>
                <div className={"red-rectangle-" + this.decorator_type}/>
                <div className={"blue-rectangle-" + this.decorator_type}/>
            </div>
        );
    }
}

TitleDecorator.propTypes = {
    top: PropTypes.number,
    left: PropTypes.number,
    position: PropTypes.string,
    decorator_type: PropTypes.string
};

TitleDecorator.defaultProps = {
    top: 0,
    left: 0,
    position: "relative"
};

export default TitleDecorator;


