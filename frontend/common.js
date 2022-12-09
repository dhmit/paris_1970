/**
 * Common.js -- miscellaneous routines useful throughout the system
 */

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

