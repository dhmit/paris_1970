import React from "react";
import ParisMap from "../components/ParisMap";
import LoadingPage from "./LoadingPage";
import * as PropTypes from "prop-types";
import PhotoViewer from "../components/PhotoViewer";

class Tags extends PhotoViewer {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            tagData: null
        };
    }

    async componentDidMount() {
        try {
            const response = await fetch(`/api/tag/${this.props.tagName}/`);
            if (!response.ok) {
                this.setState({loading: false});
            } else {
                const tagData = await response.json();
                this.setState({
                    tagData,
                    loading: false
                });
            }
        } catch (e) {
            console.log(e);
        }
    }

    formatTag(tagName) {
        let array = tagName.split(" ");
        for (let i = 0; i < array.length; i++) {
            array[i] = array[i].charAt(0).toUpperCase() + array[i].slice(1);
        }
        let result = array.join(" ");
        return result;
    }

    render() {
        if (this.state.loading) {
            return (<LoadingPage/>);
        }

        if (this.state.tagData.length === 0) {
            return (<>
                Tag {this.props.tagName} is not in the database.
            </>);
        }
        const tag = this.props.tagName;
        const photos = this.state.tagData;

        return (<>
            <div className="row">
                <div className="tag-info col-12 col-lg-5">
                    <p style={{fontSize: "30px", fontWeight: "600"}}>Photographs tagged</p>
                    <p style={{color: "#FB2F2A",fontSize: "40px", fontWeight: "800"}}>{this.formatTag(tag)}</p>
                    <>{this.getPhotoGrid(photos, {"photoSize": [120, 120]})}</>
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

Tags.propTypes = {
    tagName: PropTypes.string
};

export default Tags;
