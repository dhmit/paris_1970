import React from "react";
import {Container, Row, Col} from "react-bootstrap";
import BlogSidebar from "../components/BlogSidebar";
import * as PropTypes from "prop-types";
import {truncateText} from "../common";

function Posts(props) {
    //Display all posts
    const blogPosts = props.posts.map((post) => {
        if (post.published) {
            return (<div key={post.slug} className="card mb-4 border-0">
                    <div className="blog-post-short card-body">
                        <h1 className="blog-title">
                            <a href={post.absolute_url}>
                                {truncateText(post.title, 4)}
                            </a>
                        </h1>
                        <h5 className="blog-author">{post.author + " "}
                            <small className="text-muted">
                                {post.published ? "Published" : "Preview"} {post.date}
                            </small>
                        </h5>

                        {
                            //This apparently poses a security risk and might an outdated
                            //method for rendering raw html. May need addressing.
                        }

                        <div className="blog-text card-text" dangerouslySetInnerHTML={{
                            __html:
                                truncateText(post.content, 100, true)
                        }}
                        />
                        <a className="stretched-link text-decoration-none text-uppercase post-link"
                           href={"/blog/" + post.slug}> Read more
                        </a>
                        <div className="list-inline mb-4 mt-3">
                            {
                                //Displays tag buttons for each post
                            }
                            {post.tags.map((tag) => {
                                return (<a key={tag} className="btn btn-secondary blog-tag" href="#"
                                           role="button">{tag}</a>);
                            })}
                        </div>
                    </div>

                </div>
            );
        }
    });

    return (
        <div>{blogPosts}</div>
    );
}


class Blog extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {

        return (<Container className="blog-home" id="app_root">
                <Row>
                    <Col lg={8}>
                        <h2 className="blog-list-title">Blog</h2>
                        posts are here:::: {this.props.posts.length}
                        <Posts
                            posts={this.props.posts}
                            tags={this.props.tags}
                        />
                    </Col>
                    <Col lg={4}>
                        <BlogSidebar
                            posts={this.props.posts}
                            tags={this.props.tags}
                        />
                    </Col>
                </Row>
            </Container>
        );

    }
}

Posts.propTypes = {
    posts: PropTypes.array,
    tags: PropTypes.array
};

Blog.propTypes = {
    posts: PropTypes.array,
    tags: PropTypes.array
};

export default Blog;
