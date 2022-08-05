import React from "react";
import * as PropTypes from "prop-types";

function MapSquareList(props) {
    //Given an arrondissiment, only keeps the map squares that actually contain photos
    const mapSquareNumbers = props.arrondissementData[props.arrondissementNumber - 1]["map_square_numbers"].filter(
        number => props.filledMapSquares.has(number));

    if (mapSquareNumbers.length === 0) {
        return <span>No Map Squares!</span>;
    }

    //Returns a comma delimited list of the map square numbers in a arrondissement. Each number
    //links to corresponding map page
    const displayedMapSquares = mapSquareNumbers.map((map_square_number, i) => {
        const link = "#" + map_square_number;
        return (<span key={map_square_number}>
                        <a href={link}
                           onClick={() => props.setSelectedMapSquare(map_square_number)}
                           className="link map-square-link">{map_square_number}</a>
            {mapSquareNumbers[i + 1] ? ", " : ""}
                </span>);
    });

    return (<span>{displayedMapSquares}</span>);
}


MapSquareList.propTypes = {
    arrondissementData: PropTypes.array,
    arrondissementNumber: PropTypes.number,
    filledMapSquares: PropTypes.object,
    setSelectedMapSquare: PropTypes.func
};

export default MapSquareList;
