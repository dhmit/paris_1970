import React from "react";
import {Container, Row, Col} from "react-bootstrap";

import * as PropTypes from "prop-types";
import BlogSidebar from "../../components/BlogSidebar";

export class BlogPost extends React.Component {
    constructor(props) {
        super(props);

        console.log(this.props.all_posts);
    }

    render() {
        return this.props.post.published ? (
            <div className="blog" id="app_root">
                <Container className="mt-3">
                    <Row>
                        <Col className={"blog-post"} lg={8}>
                            {
                                //May need to change this statement. Can pose security risks and
                                //may also be outdated method of rendering raw HTML
                            }
                            <h1 className="blog-title">
                                <a href={this.props.post.absolute_url}>
                                    {this.props.post.title}
                                </a>
                            </h1>
                            <h5 className="blog-author">
                                {this.props.post.subtitle} 
                            </h5>

                            <small className="text-muted">
                                {this.props.post.published ? "Published" : "Preview"} {this.props.post.date}
                            </small>
                            <ul className="list-inline">
                                {this.props.tags.map(tag => {
                                    return <li key={tag}>
                                        <a key={tag} className="btn btn-secondary blog-tag" href="#"
                                           role="button">{tag}</a>
                                    </li>;

                                })
                                }
                            </ul>
                            <div className="blog-text"
                                 dangerouslySetInnerHTML={{__html: this.props.post.content}}
                            />
                        </Col>
                        <Col lg={4}>
                            <BlogSidebar
                                posts={this.props.all_posts}
                                tags={this.props.tags}
                            />
                        </Col>
                    </Row>
                </Container>
            </div>
        ) : (
            <div className="blog" id="app_root">
                <h5 className="important-notice">
                    This page is only a preview of the post and is only visible to the author and
                    site admin.
                    To make it visible to anyone, the author or a user with blog edit access must
                    click
                    "published" in the admin panel.
                </h5>
            </div>
        );
    }
}

BlogPost.propTypes = {
    tags: PropTypes.array,
    post: PropTypes.object,
    all_posts: PropTypes.array
};

export default BlogPost;


