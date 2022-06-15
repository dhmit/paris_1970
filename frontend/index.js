/*
 * The entrypoint for our application:
 * This module gets loaded into the DOM, and then it loads everything else.
 */
import React from "react";
import ReactDOM from "react-dom";

import Base from "./Base";
import ErrorNotFoundComponent from "./components/ErrorNotFoundComponent";

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

// Import all styles
import "./scss/styles.scss";

const COMPONENT_PROPS_RAW = document.getElementById("component_props").text;
const COMPONENT_NAME_RAW = document.getElementById("component_name").text;
const COMPONENT_PROPS = JSON.parse(COMPONENT_PROPS_RAW);
const COMPONENT_NAME = JSON.parse(COMPONENT_NAME_RAW);
const COMPONENTS = {
    ErrorNotFoundComponent,
    HomePage,
    About,
    Search,
    PhotoView,
    SimilarityView,
    PhotographerView,
    MapSquareView,
    AllAnalysisView,
    AnalysisView,
    AllPhotosView,
    ClusterView
};

const PreselectedComponent = COMPONENTS[COMPONENT_NAME || "ErrorNotFoundComponent"];

ReactDOM.render(
    <Base>
        <PreselectedComponent {...COMPONENT_PROPS} />
    </Base>,
    document.getElementById("app_root")
);
