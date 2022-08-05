/**
 * Common.js -- miscellaneous routines useful throughout the system
 */

import * as d3 from "d3";
import React from "react";


/**
 * Get the value of a cookie, given its name
 * Adapted from https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax
 * @param {string} name - The name of the cookie
 */
export function getCookie(name) {
    let cookieValue;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (const rawCookie of cookies) {
            const cookie = rawCookie.trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * This method takes GeoJSON parsed into an object,
 * projects all of the geometries from lon-lat into x-y coords in SVG-space,
 * and returns a list of objects containing these paths, and some metadata (iso, name)
 */
export function projectFeaturesCreateSVGPaths(geoJSON, width = 800, height = 800) {
    const center = [2, 15];

    const projection = d3.geoMercator()
    .center(center)
    // fitExtent documentation can be found here https://github.com/d3/d3-geo#projection_fitExtent
    .fitExtent([
            [0, 0],
            [
                width,
                height
            ]
        ],
        geoJSON);
    const geoGenerator = d3.geoPath()
    .projection(projection);

    const mapData = [];
    for (const feature of geoJSON.features) {
        const svgPath = geoGenerator(feature.geometry);
        const iso = feature.properties.ISO_A3;
        const {name} = feature.properties;
        mapData.push({
            svg_path: svgPath,
            name,
            iso
        });
    }
    return mapData;
}

/**
 * Standard js implementation of a debouncer function
 */
export function debounce(func, timeout = 300) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => {
            func.apply(this, args);
        }, timeout);
    };
}

/**
 * Given a string, returns a truncated version of the string. String is truncated based on the
 * amount of words in the string.
 *
 * @param text input string to truncate
 * @param truncate_point the numbers of words that are still maintained in the string
 * @param raw_html true if return type is a string in raw HTML format. Otherwise return type is
 *                 a JSX element
 * @returns {string|*|JSX.Element}
 */
export function truncateText(text, truncate_point,raw_html=false){
    let newText = text.split(" ");
    newText = newText.length > truncate_point ? newText.slice(0,truncate_point).join(" ") + " ..."
        : newText.join(" ");
    return (raw_html ? newText : <span> {newText} </span>);
}

