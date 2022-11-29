/*
 * The entrypoint for our application:
 * This module gets loaded into the DOM, and then it loads everything else.
 */
import React from "react";
import ReactDOM from "react-dom";

import Base from "./Base";

import {HomePage} from "./pages/Home";
import {PhotoView} from "./pages/views/PhotoView";
import {PhotographerView} from "./pages/views/PhotographerView";
import {MapSquareView} from "./pages/views/MapSquareView";
import {Search} from "./pages/Search";
import About from "./pages/About";
import Blog from "./pages/Blog";
import BlogPost from "./pages/views/BlogPostView";
import MapPage from "./pages/views/MapPageView";
import TagView from "./pages/TagView";
import {PhotographerListView} from "./pages/views/PhotographerListView";

// Import all styles
import "./scss/styles.scss";

const COMPONENT_PROPS_RAW = document.getElementById("component_props").text;
const COMPONENT_NAME_RAW = document.getElementById("component_name").text;
const COMPONENT_PROPS = JSON.parse(COMPONENT_PROPS_RAW);
const COMPONENT_NAME = JSON.parse(COMPONENT_NAME_RAW);
const COMPONENTS = {
    HomePage,
    About,
    Search,
    Blog,
    BlogPost,
    PhotoView,
    PhotographerView,
    MapSquareView,
    MapPage,
    TagView,
    PhotographerListView,
 
};

const PreselectedComponent = COMPONENTS[COMPONENT_NAME || "ErrorNotFoundComponent"];

ReactDOM.render(
    <Base>
        <PreselectedComponent {...COMPONENT_PROPS} />
    </Base>,
    document.getElementById("app_root")
);
