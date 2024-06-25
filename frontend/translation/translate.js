import React from "react";

export const Embed = (props) => {
    return (
        <a href={props.href || '#'} target="_blank" title={props.title || ''} rel="noreferrer">
            {props.children}
        </a>
    );
};
