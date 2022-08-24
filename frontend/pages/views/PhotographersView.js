import React from "react";
import * as PropTypes from "prop-types";


export class PhotographersView extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            photographers: JSON.parse(this.props.photographers)
        };
    }

    render() {
        return (<ul>
            {this.state.photographers.map(photographer => {
                return <li key={photographer.id}>
                    <a href={`/photographer/${photographer.number}`}>
                        {photographer.name}
                    </a>
                </li>;
            })}
        </ul>);
    }
}

PhotographersView.propTypes = {
    photographers: PropTypes.string
};
