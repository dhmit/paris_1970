/*
 * The entrypoint for our application:
 * This module gets loaded into the DOM, and then it loads everything else.
 */
import React from "react";
import ReactDOM from "react-dom";

import Base from "./Base";

import {HomePage} from "./pages/Home";
import {PhotoView} from "./pages/views/PhotoView";
import {SimilarityView} from "./pages/views/SimilarityView";
import {PhotographerView} from "./pages/views/PhotographerView";
import {MapSquareView} from "./pages/views/MapSquareView";
import {AnalysisView} from "./pages/views/AnalysisView";
import {AllAnalysisView} from "./pages/views/AllAnalysisView";
import {AllPhotosView} from "./pages/views/AllPhotosView";
import {ClusterView} from "./pages/views/ClusterView";
import {Search} from "./pages/Search";
import About from "./pages/About";
import MapPage from "./pages/views/MapPageView";
import TagView from "./pages/Tags";

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
    PhotoView,
    SimilarityView, //NOT NEEDED ANYMORE
    PhotographerView,
    MapSquareView,
    AllAnalysisView, //NOT NEEDED ANYMORE
    AnalysisView, //NOT NEEDED ANYMORE
    AllPhotosView,
    ClusterView, //NOT NEEDED ANYMORE
    MapPage,
    TagView
};

const PreselectedComponent = COMPONENTS[COMPONENT_NAME || "ErrorNotFoundComponent"];

ReactDOM.render(
    <Base>
        <PreselectedComponent {...COMPONENT_PROPS} />
    </Base>,
    document.getElementById("app_root")
);
