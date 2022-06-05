import React from "react";
import * as PropTypes from "prop-types";
import "./legend.scss";

export class Legend extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            labels: [],
            getColor: (d) => {
                if (d === 1) {
                    return "#E85285";
                }
                if (d === 2) {
                    return "#C9458B";
                }
                if (d === 3) {
                    return "#A93790";
                }
                if (d === 4) {
                    return "#8A2995";
                }
                return "#6A1B9A";
            }
        };
    }

    componentDidMount() {
        // get color depending on the bucket that corresponds with the number of photos
        let labels = [];
        for (let i = 0; i < 9; i += 2) {
            labels.push(i);
        }
        this.setState({
            labels: labels
        });

    };


    render() {
        return (
            <div className="heat-map-info heat-map-legend">
                <h6>Photo Density</h6>
                (photos/square)<br/>
                <ul>

                    {this.state.labels.map((item) => {
                        return <li key={item}>
                            <i style={{"background": this.state.getColor(item + 1)}}/>
                            {this.props.buckets[item]} &ndash; {this.props.buckets[item + 1]}
                        </li>;
                    })}
                </ul>
            </div>
        );
    }
}

Legend.propTypes = {
    buckets: PropTypes.array
};

export default Legend;

