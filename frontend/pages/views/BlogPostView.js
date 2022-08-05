import React from "react";
import * as PropTypes from "prop-types";

export class BlogPost extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            tags: props.tags,
            post: props.post
        };
    }

    render() {
        return (
            <p>milk</p>
        );
    }
}

BlogPost.propTypes = {
    tags: PropTypes.array,
    post: PropTypes.object
};

export default BlogPost;


