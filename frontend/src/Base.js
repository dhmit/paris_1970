import React from "react";
import * as PropTypes from "prop-types";

const Base = ({children}) => {
    return (
        <>
            <div id="main-container">
                <main role="main">{children}</main>
            </div>
        </>
    );
};

Base.propTypes = {
    children: PropTypes.object
};


export default Base;
