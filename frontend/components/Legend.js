import React from "react";
import * as PropTypes from "prop-types";
import "../scss/legend.scss";


export class Legend extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="legend">
                <h6 className="text-uppercase">Legend</h6>
                <ul>
                    {this.props.layers.map(layer => {
                        return <li key={layer}>
                            <button data-value={layer}
                                    onClick={(e) => this.props.toggleLayer(e)}
                                    className={`legend-square
                                    ${layer.toLowerCase()}
                                    ${this.props.visibleLayers.indexOf(layer) > -1 ? "" : "inactive"}`}/>


                            <span className={"label"}>{layer}</span>
                        </li>;

                    })}
                </ul>
            </div>
        );
    }
}

Legend.propTypes = {
    layers: PropTypes.array,
    visibleLayers: PropTypes.array,
    toggleLayer: PropTypes.func
};

export default Legend;

