import React from "react";
import Logo_Gif from "../images/gif/rec-animation-english---Copy.gif";

export class Loading extends React.Component {
    render() {
        const { fancy } = this.props;

        return (
            <div className="d-flex justify-content-center align-items-center" style={{ height: '100%' }}>
                {fancy ? (
                    <img src={Logo_Gif} alt="Loading..." style={{maxWidth: '100%', maxHeight: '100%', objectFit: 'contain'}} />
                ) : (
                    <div className="spinner-border" role="status">
                        <span className="visually-hidden-focusable">Loading...</span>
                    </div>
                )}
            </div>
        );
    }
}

export default Loading;
