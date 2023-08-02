/*
 * The entrypoint for our application:
 * This module gets loaded into the DOM, and then it loads everything else.
 */
import * as React from "react";
import * as ReactDOM from "react-dom";

import Base from "./Base";

import About from "./pages/About";
import Explore from "./pages/Explore";
import Blog from "./pages/Blog";
import BlogPost from "./pages/BlogPostView";
import MapPage from "./pages/MapPageView";
import TagView from "./pages/TagView";
import {HomePage} from "./pages/Home";
import {MapSquareView} from "./pages/MapSquareView";
import {PhotoView} from "./pages/PhotoView";
import {PhotographerListView} from "./pages/PhotographerListView";
import {PhotographerView} from "./pages/PhotographerView";
import {Search} from "./pages/Search";
import {SimilarityView} from "./pages/SimilarityView";
import {TextOCRView} from "./pages/TextOCRView";

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
    Explore,
    HomePage,
    MapPage,
    MapSquareView,
    PhotoView,
    PhotographerListView,
    PhotographerView,
    Search,
    SimilarityView,
    TagView,
    TextOCRView,
};

const PreselectedComponent = COMPONENTS[COMPONENT_NAME];

ReactDOM.render(
    <Base>
        <PreselectedComponent {...COMPONENT_PROPS} />
    </Base>,
    document.getElementById("app_root")
);
