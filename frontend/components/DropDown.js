import React from "react";
import * as PropTypes from "prop-types";


export class DropDown extends React.Component {
    
    render () {
        return(
           <div className="dropdown-container">
                <div className="dropdown-select">
                    <p>hi</p>
                    <p>hi</p>
                </div>
                <div className="dropdown-items">
                    <p>1</p>
                    <p>2</p>
                    <p>3</p>
                </div>
           </div>
        );
    }
}

DropDown.propTypes = {
    options: PropTypes.string,
};
