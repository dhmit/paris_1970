/**
 * Common.js -- miscellaneous routines useful throughout the system
 */

import * as d3 from 'd3';


/**
 * Get the value of a cookie, given its name
 * Adapted from https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax
 * @param {string} name - The name of the cookie
 */
export function getCookie(name) {
    let cookieValue;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (const raw_cookie of cookies) {
            const cookie = raw_cookie.trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
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
export function project_features_and_create_svg_paths(geo_json, width = 800, height = 800) {
    const center = [2, 15];

    const projection = d3.geoMercator()
        .center(center)
        // fitExtent documentation can be found here https://github.com/d3/d3-geo#projection_fitExtent
        .fitExtent([
            [0, 0],
            [
                width,
                height,
            ],
        ],
        geo_json);
    const geoGenerator = d3.geoPath().projection(projection);

    const map_data = [];
    for (const feature of geo_json.features) {
        const svg_path = geoGenerator(feature.geometry);
        const iso = feature.properties.ISO_A3;
        const { name } = feature.properties;
        map_data.push({ svg_path, name, iso });
    }
    return map_data;
}

