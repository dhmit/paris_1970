import React from "react";

export class Loading extends React.Component {
    render() {
        return (
            <div className="text-center">
                <div className="spinner-border" role="status">
                    <span className="visually-hidden-focusable">Loading...</span>
                </div>
            </div>
        );
    }
}

export default Loading;
