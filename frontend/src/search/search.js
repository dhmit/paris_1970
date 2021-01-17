import React from 'react';
import PropTypes from 'prop-types';
import { Navbar, Footer, LoadingPage } from '../UILibrary/components';
import { getSource } from '../analysisView/analysisView';

class SearchForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            keyword: '',
            photographer: '',
            caption: '',
            tags: [],
            tagFilter: '',
        };
    }

    handleChange = (event) => {
        this.setState({
            ...this.state,
            [event.target.name]: event.target.value,
        });
    };

    handleSearch = async (body) => {
        const searchResponse = await fetch('/api/search/', {
            method: 'POST',
            body: JSON.stringify(body),
        });
        const searchData = await searchResponse.json();
        let searchText = searchData.length + ' photographs';
        if (body.keyword) {
            searchText += ' found with keyword \'' + body.keyword + '\'';
        }
        if (body.photographer) {
            searchText += ' by ' + body.photographer;
        }
        if (body.caption) {
            searchText += ' containing caption \'' + body.caption + '\'';
        }
        if (body.tags && body.tags.length > 0) {
            searchText += ' with tags [' + body.tags + ']';
        }
        this.props.updateSearchData({
            data: searchData,
            isAdvanced: body.isAdvanced,
            searchText,
        });
    };

    handleMultiSelectChange = (event) => {
        const value = Array.from(event.target.selectedOptions, (option) => option.value);
        this.setState({
            ...this.state,
            tags: value,
        });
    }

    handleFullTextSubmit = async (event) => {
        event.preventDefault();
        if (this.state.keyword) {
            await this.handleSearch({
                keyword: this.state.keyword.trim(),
                isAdvanced: false,
            });
        }
    };

    handleAdvancedSubmit = async (event) => {
        event.preventDefault();
        if (this.state.photographer.trim() || this.state.caption.trim()
            || this.state.tags.length > 0) {
            await this.handleSearch({
                photographer: this.state.photographer,
                caption: this.state.caption,
                tags: this.state.tags,
                isAdvanced: true,
            });
        }
    };

    handleSingleSelect = (event) => {
        // for photographer select, needs to delete the alert
        alert('You selected ' + this.state.value);
        event.preventDefault();
    }

    // When it comes to separating the advanced search and full text search ("normal" search),
    // should we split the two forms? I think this would work with the same submit button
    render() {
        const filteredTagData = this.props.tagData.filter(
            (tag) => tag.toLowerCase().includes(this.state.tagFilter.toLowerCase())
        );

        return (
            <div>
                {/* Full-Text Form */}
                <form onSubmit={this.handleFullTextSubmit}>
                    <h3>Full Text Search</h3>
                    <label>
                        <input
                            type="text"
                            name="keyword"
                            value={this.state.keyword}
                            onChange={this.handleChange}
                        />
                    </label>
                    <br />
                    <input type="submit" value="Search" />
                </form>
                {/* Advanced Search Form */}
                <br/><br/>
                <form onSubmit={this.handleAdvancedSubmit}>
                    <h3>Advanced Search</h3>
                    <label>
                        <p>Photographer:&nbsp;
                            <select value={this.state.value} onChange={this.handleChange}>
                            <option value="grapefruit">Grapefruit</option>
                            <option value="lime">Lime</option>
                            <option value="coconut">Coconut</option>
                            <option value="mango">Mango</option>
                            </select>
                        </p>
                    </label>
                    <br/>
                    <label>
                        <p>Caption:</p>
                        <input
                            type="text"
                            name="caption"
                            value={this.state.caption}
                            onChange={this.handleChange}
                        />
                    </label>
                    <br/>
                    <label>
                        <p>Tags:</p>
                        <input
                            type="text"
                            name="tagFilter"
                            value={this.state.tagFilter}
                            onChange={this.handleChange}
                        />
                        <br/>
                        <select
                            name="tags"
                            className='tag-selection'
                            multiple={true}
                            value={this.state.tags}
                            onChange={this.handleMultiSelectChange}
                        >
                            {
                                filteredTagData.map((tagData, key) => {
                                    return (
                                        <option value={tagData} key={key}>
                                            {tagData}
                                        </option>
                                    );
                                })
                            }
                        </select>
                    </label>
                    <br/>
                    <input type="submit" value="Search" />
                </form>
            </div>
        );
    }
}
SearchForm.propTypes = {
    updateSearchData: PropTypes.func,
    tagData: PropTypes.array,
};

export class Search extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            data: null,
            isAdvanced: false,
            searchedText: '',
            tagData: null,
            photographerData: null,
        };
    }

    updateSearchData = (searchData) => {
        this.setState({ ...searchData });
    }

    async componentDidMount() {
        try {
            const tagResponse = await fetch('/api/get_tags/');
            const tagData = await tagResponse.json();
            const photographerResponse = await fetch('/api/all_photographers/');
            const photographerData = await photographerResponse.json();
            this.setState({ photographerData, tagData, loading: false });
        } catch (e) {
            console.log(e);
        }
    }

    // This follows the full text + advanced search model here: http://photogrammar.yale.edu/search/
    render() {
        if (!this.state.tagData) {
            return (<LoadingPage/>);
        }
        return (
            <>
                <Navbar />
                <div className='search-page page row'>
                    <div className='col-sm-12 col-lg-4 search-form'>
                        <h1>Search</h1>
                        <SearchForm
                            updateSearchData={this.updateSearchData}
                            tagData={this.state.tagData}
                        />
                    </div>
                    <div className='col-sm-12 col-lg-8'>
                        {
                            this.state.data
                            && <div>
                                <h2>
                                    {this.state.isAdvanced
                                        ? 'Advanced Search Results'
                                        : 'Search Results'}
                                </h2>
                                <p>{this.state.searchText}</p>
                                <div className='search-results'>
                                    {this.state.data.map((photo, k) => {
                                        const photoId = `${photo['map_square_number']}`
                                                      + `/${photo['number']}`;
                                        if (photo.cleaned_src || photo.front_src) {
                                            return (
                                                <a
                                                    key={k}
                                                    title={'Map Square: '
                                                           + photo['map_square_number']
                                                           + ', Number: ' + photo['number']}
                                                    href={'/photo/' + photoId + '/'}
                                                >
                                                    <img
                                                        alt={photo.alt}
                                                        height={150}
                                                        width={150}
                                                        src={getSource(photo)}
                                                    />
                                                </a>
                                            );
                                        }
                                        return '';
                                    })}
                                </div>
                            </div>
                        }
                    </div>
                </div>
                <Footer />
            </>

        );
    }
}
