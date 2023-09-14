import React from "react";
import * as PropTypes from "prop-types";

export class BlogSidebar extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            tags: props.tags,
            posts: props.posts
        };
    }


    render() {
        return (
            <div className="blog-sidebar">
                <div className="card mb-4 border-0">
                    <div className="card-body">
                        <div className="title mb-1 fw-bold">Posts</div>
                        <ul className="list-unstyled mb-0">
                            {this.state.posts.map((post) => {
                                if(post.published) {
                                    return (
                                        //outputs a list of post links
                                        <li key={post.slug} className="blog-sidebar-post-list">
                                            <a className="post-link" href={"/articles/" + post.slug}>
                                                {post.title}
                                            </a>
                                        </li>);
                                }
                            })}
                        </ul>
                    </div>
                </div>
            </div>
        );
    }
}

BlogSidebar.propTypes = {
    posts: PropTypes.array,
    tags: PropTypes.array
};

export default BlogSidebar;


