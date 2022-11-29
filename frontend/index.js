/*
 * The entrypoint for our application:
 * This module gets loaded into the DOM, and then it loads everything else.
 */
import React from "react";
import ReactDOM from "react-dom";

import Base from "./Base";

import About from "./pages/About";
import Blog from "./pages/Blog";
import BlogPost from "./pages/views/BlogPostView";
import Logo from "./components/Logo";
import MapPage from "./pages/views/MapPageView";
import TagView from "./pages/TagView";
import {HomePage} from "./pages/Home";
import {MapSquareView} from "./pages/views/MapSquareView";
import {PhotoView} from "./pages/views/PhotoView";
import {PhotographerListView} from "./pages/views/PhotographerListView";
import {PhotographerView} from "./pages/views/PhotographerView";
import {Search} from "./pages/Search";
import {SimilarityView} from "./pages/views/SimilarityView";
import {TextOCRView} from "./pages/views/TextOCRView";

// Import all styles
import "./scss/styles.scss";

const COMPONENT_PROPS_RAW = document.getElementById("component_props").text;
const COMPONENT_NAME_RAW = document.getElementById("component_name").text;
const COMPONENT_PROPS = JSON.parse(COMPONENT_PROPS_RAW);
const COMPONENT_NAME = JSON.parse(COMPONENT_NAME_RAW);
const COMPONENTS = {
    About,
    Blog,
    BlogPost,
    HomePage,
    Logo,
    MapPage,
    MapSquareView,
    PhotoView,
    PhotographerListView,
    PhotographerView,
    Search,
    SimilarityView,
    TagView,
    PhotographerListView,
    TextOCRView,
};

const PreselectedComponent = COMPONENTS[COMPONENT_NAME || "ErrorNotFoundComponent"];

ReactDOM.render(
    <Base>
        <PreselectedComponent {...COMPONENT_PROPS} />
    </Base>,
    document.getElementById("app_root")
);
