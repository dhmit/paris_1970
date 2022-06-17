import React from "react";

export class Loading extends React.Component {
    render() {
        return (
            <div className="m-auto">
                <div className="spinner-border" role="status">
                    <span className="sr-only">Loading...</span>
                </div>
            </div>
        );
    }
}

export default Loading;
