import React, { Component } from 'react';
import * as PropTypes from 'prop-types';
import DataContainer from './DataContainer';

class searchApp extends React.Component {
    state = {
        searchTerm: '',
        searchDataArray: [],
    }

    editSearch = (e) => {
        this.setState({searchTerm: e.target.value})
    }

    dynamicSearch = () => {
        return this.state.searchDataArray.filter(data => name.toLowerCase().includes(this.state.searchTerm.toLowerCase()))
    }

    render() {
        const searchData = Object.values(this.props.searchData);
        for (const key in searchData) {
            this.searchDataArray.push(this.searchData[key]);
        }

        return (
            <div style = {{textAlign: 'center', paddingTop: '30vh'}}>
                <input type = 'text' value = {this.state.searchTerm} onChange = {this.editSearch} placeholder = 'Search for a name!' />
                <DataContainer data = {this.dynamicSearch()} />
            </div>
        )
    }


}

export default searchApp;
