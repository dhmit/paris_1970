import React from "react";
import * as PropTypes from "prop-types";
import {Container} from "react-bootstrap";
import {truncateText} from "../common";

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
                        <div className="card-title mb-1 fw-bold">Tags</div>
                        <Container>
                            {this.state.tags.map((tag) => {
                                return(
                                    //outputs a list of tag buttons
                                    <a key={tag.id} className="btn btn-secondary btn-sm blog-sidebar-tag-button"
                                       href="#"
                                       role="button">{tag}</a>);
                            })}
                        </Container>
                    </div>
                </div>

                <div className="card mb-4 border-0">
                    <div className="card-body">
                        <div className="title mb-1 fw-bold">Posts</div>
                        <ul className="list-unstyled mb-0">
                            {this.state.posts.map((post) => {
                                if(post.published) {
                                    return (
                                        //outputs a list of post links
                                        <li key={post.slug} id="blog-sidebar-post-list">
                                            <a className="post-link" href={"/blog/" + post.slug}>
                                                {truncateText(post.title,4)}
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


