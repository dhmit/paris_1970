import React from "react";
import ParisMap from "../components/ParisMap";

class Tags extends React.Component {
    render() {
        return (<>
            <div className="row">
                <div className="tag-info col-12 col-lg-5">
                    <p style={{fontSize: "30px", fontWeight: "600"}}>Photographs tagged</p>
                    <p style={{color: "#FB2F2A",fontSize: "40px", fontWeight: "800"}}>Construction</p>
                </div>
                <div className="tag-map col-12 col-lg-7">
                    <ParisMap
                        className="tags-map"
                        zoom={14}
                        layers={{ }}
                    />
                </div>
            </div>
        </>);
    }
}

export default Tags;
