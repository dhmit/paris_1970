import React from 'react';
import * as PropTypes from 'prop-types';

export class AnalysisWidget extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            view: 0,
        };
    }
    
    toggleStatus = (event) => {
         this.setState({
             view: parseInt(event.target.value)
         });
    }

    render() {
        return (
            <div className="row">
                <div className="col-6">
                    <select id="toggleSelect" className="custom-select" onChange={this.toggleStatus} value={this.state.value}>
                        <option value="0">Select...</option>
                        <option value="1">Perspective Lines</option>
                        <option value="2">Foreground Mask</option>
                    </select>
                </div>
            </div>
        );
    }
}
