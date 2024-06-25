import React from "react";
import {Container, Row, Col} from "react-bootstrap";
import BlogSidebar from "../components/BlogSidebar";
import * as PropTypes from "prop-types";
import {truncateText} from "../common";
import { Trans, withTranslation } from "react-i18next";
import { Embed } from "../translation/translate";

function Posts(props) {
    //Display all posts
    const blogPosts = props.posts.map((post) => {
        if (post.published) {
            return (<div key={post.slug} className="card mb-4 border-0">
                    <div className="blog-post-short card-body">
                        <h1 className="blog-title">
                            <a href={post.absolute_url}>
                                {post.title}
                            </a>
                        </h1>
                        <h5 className="blog-author">
                            {post.subtitle}<br/>
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
                           href={"/articles/" + post.slug}> {props.t('Blog.readMore')}
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


class BaseBlog extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {

        return (<Container className="blog-home" id="app_root">
                <Row>
                    <Col lg={8}>
                        <h2 className="blog-list-title">{this.props.t('Blog.title')}</h2>
                        <p><Trans
                            i18nKey='Blog.header' // optional -> fallbacks to defaults if not provided
                            components={{
                                link1: <Embed href="https://history.mit.edu/people/catherine-clark/" target="_blank" rel="noreferrer"/>
                            }}
                        /></p>

                        <Posts
                            posts={this.props.posts}
                            tags={this.props.tags}
                            t={this.props.t}
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

BaseBlog.propTypes = {
    posts: PropTypes.array,
    tags: PropTypes.array
};

const Blog = withTranslation()(BaseBlog);
export default Blog;
