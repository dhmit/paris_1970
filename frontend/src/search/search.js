import React from 'react';
import Select from 'react-select';
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
        };
    }

    handleChange = (event) => {
        this.setState({
            ...this.state,
            [event.target.name]: event.target.value,
        });
    };

    handleSelectDropdownChange = (selectedOptions) => {
        this.setState({
            ...this.state,
            tags: selectedOptions,
        });
    }

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
        if (body.photographerName || body.photographerId) {
            if (!body.photographerId) {
                searchText += ' by ' + body.photographerName;
            } else if (!body.photographerName) {
                searchText += ' by #' + body.photographerId;
            } else {
                searchText += ' by ' + body.photographerName + ' (#' + body.photographerId + ')';
            }
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
            [event.target.name]: value,
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
            const photographerParts = this.state.photographer.split(',');
            const photographerName = photographerParts[0] ? photographerParts[0] : '';
            const photographerId = photographerParts[1] ? photographerParts[1] : '';
            const newTags = [];
            for (const tag of this.state.tags) {
                newTags.push(tag.value);
            }
            await this.handleSearch({
                photographerName,
                photographerId,
                caption: this.state.caption,
                tags: newTags,
                isAdvanced: true,
            });
        }
    };

    render() {
        const tagOptions = this.props.tagData.map((tag) => ({value: tag, label: tag}));

        const photographerData = this.props.photographerData;

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
                            <select
                                value={this.state.photographer}
                                onChange={this.handleChange}
                                name="photographer"
                            >
                                <option value="">None</option>
                                {
                                    photographerData.map((photographer, key) => {
                                        const valueArray = [photographer.name, photographer.number];

                                        if (photographer.name.length === 0) {
                                            return (
                                                <option value={valueArray} key={key}>
                                                    Unknown [{photographer.number}]
                                                </option>
                                            );
                                        }
                                        if (photographer.number === null) {
                                            return (
                                                <option value={valueArray} key={key}>
                                                    {photographer.name} [Unknown]
                                                </option>
                                            );
                                        }
                                        return (
                                            <option value={valueArray} key={key}>
                                                {photographer.name} [{photographer.number}]
                                            </option>
                                        );
                                    })
                                }
                            </select>
                        </p>
                    </label>
                    <br/>
                    <label>
                        <p>Caption:&nbsp;
                            <input
                                type="text"
                                name="caption"
                                value={this.state.caption}
                                onChange={this.handleChange}
                            />
                        </p>
                    </label>
                    <br/>
                    <label>
                        <p>Tags:</p>
                        <Select
                            defaultValue={this.state.tags}
                            isMulti
                            name="tags"
                            options={tagOptions}
                            onChange={this.handleSelectDropdownChange}
                        />
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
    photographerData: PropTypes.array,
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
            const searchTagResponse = await fetch('/api/get_tags/');
            const searchTags = await searchTagResponse.json();
            const { tags, photographers } = searchTags;
            this.setState({ photographerData: photographers, tagData: tags, loading: false });
        } catch (e) {
            console.log(e);
        }
    }

    // This follows the full text + advanced search model here: http://photogrammar.yale.edu/search/
    render() {
        if (!this.state.tagData || !this.state.photographerData) {
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
                            photographerData={this.state.photographerData}
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
                                        if (photo.cleaned_src || photo.front_src
                                            || photo.binder_src) {
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
                                                        height={120}
                                                        width={120}
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
