import React, { Component } from 'react';
import sData from './sData';

class DataContainer extends Component {
    render() {
        return (
            <div>
                {this.props.searchDataArray.map(data => <sData data = {data} />)}
            </div>
        )
    }
}

export default DataContainer;
