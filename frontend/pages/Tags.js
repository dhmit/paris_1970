import React from "react";
import ParisMap from "../components/ParisMap";
import LoadingPage from "./LoadingPage";
import * as PropTypes from "prop-types";

class Tags extends React.Component {
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

        return (<>
            <div className="row">
                <div className="tag-info col-12 col-lg-5">
                    <p style={{fontSize: "30px", fontWeight: "600"}}>Photographs tagged</p>
                    <p style={{color: "#FB2F2A",fontSize: "40px", fontWeight: "800"}}>{tag.charAt(0).toUpperCase() +
                        tag.slice(1)}</p>
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
