/*
 * The entrypoint for our application:
 * This module gets loaded into the DOM, and then it loads everything else.
 */
import React from 'react';
import ReactDOM from 'react-dom';

import 'bootstrap/dist/css/bootstrap.min.css';

import { IndexView } from './index/index';
import { PhotoView } from './photoView/photoView';
import { SimilarityView } from './similarityView/similarityView';
import { PhotographerView } from './photographerView/photographerView';
import { MapSquareView } from './mapSquareView/mapSquareView';
import { AnalysisView } from './analysisView/analysisView';
import { AllPhotosView } from './similarityView/allPhotosView';
import About from './about/about';

// Import all styles
import './UILibrary/styles.scss';

window.app_modules = {
    React,  // Make React accessible from the base template
    ReactDOM,  // Make ReactDOM accessible from the base template

    // Add all frontend views here
    IndexView,
    About,
    PhotoView,
    SimilarityView,
    PhotographerView,
    MapSquareView,
    AnalysisView,
    AllPhotosView,
};
