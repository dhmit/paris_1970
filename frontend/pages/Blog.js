import React from "react";
import {Container, Row, Col} from "react-bootstrap";
import * as PropTypes from "prop-types";

function Posts(props){

    function truncateText(text, truncate_point,raw_html=false){
        let newText = text.split(" ");
        newText = newText.length > truncate_point ? newText.slice(0,truncate_point).join(" ") + " ..."
            : newText.join(" ");
        console.log(props.tags);
        return (raw_html ? newText : <span> {newText} </span>);
    }

    const blogPosts = props.posts.map((post) => {
        if(post.published){
            return(<div key={post.slug} className="card mb-4 border-0">
                        <div className="card-body">
                            <a href={post.absolute_url}>
                                    <h1 className="card-title">
                                        {truncateText(post.title,4)}
                                    </h1>
                            </a>
                            <h5 className="blog-author">{post.author + " "}
                                <small className="text-muted">
                                    {post.published ? "True" : "False"}
                                </small>
                            </h5>
                            {
                                //This apparently poses a security risk and might an outdated
                                //method for rendering raw html. May need addressing.
                            }
                            <p className="card-text"/>
                            <div dangerouslySetInnerHTML={{__html:
                                    truncateText(post.content,100, true)}}
                                 />
                            <a className="stretched-link text-decoration-none text-uppercase blog-post-read-more"
                               href={"/blog/"+post.slug}> Read more
                            </a>
                            <div className="list-inline mb-4 mt-3">
                                {post.tags.map((tag) => {
                                    return(<a key={tag} className="btn btn-secondary blog-tag" href="#"
                                       role="button">{tag}</a>);
                                })}
                            </div>
                        </div>

                   </div>
            );
        }
    });

    return(
        <div>{blogPosts}</div>
    );
}



class Blog extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {

        return(<Container className="blog-home" id="app_root">
                    <Row>
                        <Col lg={8}>
                            <h2 className="blog-list-title">Blog</h2>
                            <Posts
                                posts={this.props.posts}
                                tags={this.props.tags}
                            />
                        </Col>
                        <Col lg={4} >
                            <h2>Blog Sidebar Placeholder</h2>
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
