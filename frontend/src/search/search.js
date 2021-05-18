import React from 'react';
import Select from 'react-select';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';
import Input from '@material-ui/core/Input';
import { Navbar, Footer, LoadingPage } from '../UILibrary/components';
import { getSource } from '../analysisView/analysisView';

const useStyles = makeStyles({
  root: {
    width: 250,
  },
  input: {
    width: 42,
  },
});

function AnalysisSlider(props) {
        const classes = useStyles();
        const [value, setValue] = React.useState(30);

        const handleSliderChange = (event, newValue) => {
            setValue(newValue);
        };

        const handleInputChange = (event) => {
            setValue(event.target.value === '' ? '' : Number(event.target.value));
        };

        const handleBlur = () => {
            if (value < 0) {
                setValue(0);
            } else if (value > 100) {
                setValue(100);
            }
        };

        return (
            <div className={classes.root}>
                <Typography id="input-slider" gutterBottom>
                    {props.analysisName}
                </Typography>
                <Grid container spacing={2} alignItems="center">
                    <Grid item xs>
                        <Slider
                            value={typeof value === 'number' ? value : 0}
                            onChange={handleSliderChange}
                            aria-labelledby="input-slider"
                        />
                    </Grid>
                    <Grid item>
                        <Input
                            className={classes.input}
                            value={value}
                            margin="dense"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            inputProps={{
                                'step': 1,
                                'min': 0,
                                'max': 100,
                                'type': 'number',
                                'aria-labelledby': 'input-slider',
                            }}
                        />
                    </Grid>
                </Grid>
            </div>
        );
    }

AnalysisSlider.propTypes = {
    analysisName: PropTypes.string,
};

// function AnalysisSliders(props) {
//     console.log('hello its me');
//     console.log(props.analysisNames);
//     const sliders = [];
//     for (let i = 0; i < props.analysisNames.length; i++) {
//         sliders.push(<AnalysisSlider key={i} analysisName={props.analysisNames[i]}/>);
//     }
//     console.log('i am a slider');
//     console.log(sliders);
//     return sliders;
// }

// AnalysisSliders.propTypes = {
//     analysisNames: PropTypes.arrayOf(PropTypes.string),
// };

class SearchForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            keyword: '',
            photographer: '',
            caption: '',
            tags: [],
            analysisTags: [],
            sliderValues: {},
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

    handleAnalysisSelectDropdownChange = (selectedOptions) => {
        const newSliderValues = {};
        const analysisTagValues = this.getTagValues(selectedOptions);
        for (const analysisName of analysisTagValues) {
            if (analysisName in this.state.sliderValues) {
                newSliderValues[analysisName] = this.state.sliderValues[analysisName];
            } else if (analysisName in this.props.analysisValueRanges) {
                const [minValue, maxValue] = this.props.analysisValueRanges[analysisName];
                newSliderValues[analysisName] = [minValue, maxValue];
            }
        }
        this.setState({
            ...this.state,
            analysisTags: selectedOptions,
            sliderValues: newSliderValues,
        });
    }

    handleSearch = async (body) => {
        const searchResponse = await fetch('/api/search/', {
            method: 'POST',
            body: JSON.stringify(body),
        });
        console.log('Called handle search');
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
        if (body.analysisTags && body.analysisTags.length > 0) {
            searchText += ' with result for [' + body.analysisTags + ']';
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

    setSliderValue(analysisName, newLowerBound, newUpperBound) {
        const newSliderValues = this.state.sliderValues;
        if (newLowerBound === null) {
            newLowerBound = this.state.sliderValues[0];
        }
        if (newUpperBound === null) {
            newUpperBound = this.state.sliderValues[1];
        }
        newSliderValues[analysisName] = [newLowerBound, newUpperBound];
        this.setState({
            ...this.state,
            sliderValues: newSliderValues,
        });
    }

    handleSliderChange = (event, value, analysisName) => {
        console.log(value);
        const [newLowerBound, newUpperBound] = value;
        this.setSliderValue(analysisName, newLowerBound, newUpperBound);
    }

    handleSliderInputChange = (event, analysisName, bound) => {
        const [minValue, maxValue] = this.props.analysisValueRanges[analysisName];
        const newSliderValues = this.state.sliderValues;
        if (event.target.value !== '' && bound === 'lower' && Number(event.target.value) >= minValue) {
            let newValue = Number(event.target.value);
            if (newValue > this.state.sliderValues[analysisName][1]) {
                newValue = this.state.sliderValues[analysisName][1];
            }
            newSliderValues[analysisName] = [newValue, this.state.sliderValues[analysisName][1]];
        } else if (event.target.value !== '' && bound === 'upper' && Number(event.target.value) <= maxValue) {
            let newValue = Number(event.target.value);
            if (newValue < this.state.sliderValues[analysisName][0]) {
                newValue = this.state.sliderValues[analysisName][0];
            }
            newSliderValues[analysisName] = [this.state.sliderValues[analysisName][0], newValue];
        }
        this.setState({
            ...this.state,
            sliderValues: newSliderValues,
        });
    };

    handleSliderBlur = (analysisName) => {
        const [minValue, maxValue] = this.props.analysisValueRanges[analysisName];
        if (this.state.sliderValues[analysisName][0] < minValue) {
            this.setSliderValue(analysisName, minValue, null);
        } else if (this.state.sliderValues[analysisName][1] > maxValue) {
            this.setSliderValue(analysisName, null, maxValue);
        }
    };

    getTagValues(selectedOptions) {
        const newTags = [];
        // console.log(selectedOptions);
        if (selectedOptions) {
            for (const tag of selectedOptions) {
                newTags.push(tag.value);
            }
        }
        return newTags;
    }

    getPhotoTagValues() {
        return this.getTagValues(this.state.tags);
    }

    getAnalysisTagValues() {
        const newAnalysisTags = [];
        // console.log(this.state.analysisTags);
        if (this.state.analysisTags) {
            for (const atag of this.state.analysisTags) {
                newAnalysisTags.push(this.props.analysisTagMap[atag.value]);
            }
        }
        return newAnalysisTags;
    }

    handleAdvancedSubmit = async (event) => {
        event.preventDefault();
        if (this.state.photographer.trim() || this.state.caption.trim()
            || (this.state.tags && this.state.tags.length > 0)
            || (this.state.analysisTags && this.state.analysisTags.length > 0)) {
            const photographerParts = this.state.photographer.split(',');
            const photographerName = photographerParts[0] ? photographerParts[0] : '';
            const photographerId = photographerParts[1] ? photographerParts[1] : '';
            const newTags = this.getPhotoTagValues();
            const newAnalysisTags = this.getAnalysisTagValues();
            const sliderSearchValues = {};
            for (const atag in this.state.sliderValues) {
                if (this.state.sliderValues) {
                    sliderSearchValues[this.props.analysisTagMap[atag]] = this.state.sliderValues[atag];
                }
            }
            await this.handleSearch({
                photographerName,
                photographerId,
                caption: this.state.caption,
                tags: newTags,
                isAdvanced: true,
                analysisTags: newAnalysisTags,
                sliderSearchValues: sliderSearchValues,
            });
        }
    };

    render() {
        const tagOptions = this.props.tagData.map((tag) => ({ value: tag, label: tag }));
        const analysisTagOptions = this.props.analysisTagData.map((tag) => ({ value: tag, label: tag }));

        const photographerData = this.props.photographerData;

        const sliders = [];
        if (this.state.analysisTags) {
            console.log(this.props.analysisValueRanges);
            // console.log(Object.values(this.state.analysisTags));
            const currentAnalysisTags = this.getTagValues(this.state.analysisTags);
            for (let i = 0; i < currentAnalysisTags.length; i++) {
                if (currentAnalysisTags[i] in this.props.analysisValueRanges) {
                    const analysisName = currentAnalysisTags[i];
                    const sliderValue = this.state.sliderValues[analysisName];
                    const [minValue, maxValue] = this.props.analysisValueRanges[analysisName];
                    // console.log(this.state.sliderValues);
                    sliders.push(
                        <div key={analysisName}>
                            <Typography id="range-slider" gutterBottom>
                                {analysisName}
                            </Typography>
                            <Grid container spacing={2} alignItems="center">
                                <Grid item>
                                    <Input
                                        value={sliderValue[0]}
                                        margin="dense"
                                        onChange={(e) => this.handleSliderInputChange(e, analysisName, 'lower')}
                                        onBlur={() => this.handleSliderBlur(analysisName)}
                                        inputProps={{
                                            'step': 1,
                                            'min': minValue,
                                            'max': maxValue,
                                            'type': 'number',
                                            'aria-labelledby': 'input-slider',
                                        }}
                                    />
                                </Grid>
                                <Grid item xs>
                                    <Slider
                                        value={typeof sliderValue === 'object' ? sliderValue : [minValue, maxValue]}
                                        onChange={(e, v) => this.handleSliderChange(e, v, analysisName)}
                                        min={minValue}
                                        max={maxValue}
                                        valueLabelDisplay="auto"
                                        aria-labelledby="range-slider"
                                    />
                                </Grid>
                                <Grid item>
                                    <Input
                                        value={sliderValue[1]}
                                        margin="dense"
                                        onChange={(e) => this.handleSliderInputChange(e, analysisName, 'upper')}
                                        onBlur={() => this.handleSliderBlur(analysisName)}
                                        inputProps={{
                                            'step': 1,
                                            'min': minValue,
                                            'max': maxValue,
                                            'type': 'number',
                                            'aria-labelledby': 'input-slider',
                                        }}
                                    />
                                </Grid>
                            </Grid>
                        </div>
                        );
                }
            }
        }

        return (
            <div>
                {/* Full-Text Form */}
                <form onSubmit={this.handleFullTextSubmit}>
                    <h3>Full Text Search</h3>
                    <label className='input-div'>
                        <input
                            className='search-text-input'
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
                <form onSubmit={this.handleAdvancedSubmit}>
                    <h3>Advanced Search</h3>
                    <label className='input-div'>
                        <p className='search-label'>Photographer:</p>
                        <select
                            className='search-text-input'
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
                    </label>
                    <br/>
                    <label className='input-div'>
                        <p className='search-label'>Caption:</p>
                        <input
                            className='search-text-input'
                            type="text"
                            name="caption"
                            value={this.state.caption}
                            onChange={this.handleChange}
                        />
                    </label>
                    <br/>
                    <label className='input-div'>
                        <p className='search-label'>Tags:</p>
                        <Select
                            defaultValue={this.state.tags}
                            isMulti
                            name="tags"
                            options={tagOptions}
                            onChange={this.handleSelectDropdownChange}
                            menuPlacement="auto"
                            menuPosition="fixed"
                        />
                    </label>
                    <br/>
                    <label className='input-div'>
                        <p className='search-label'>Analysis Names:</p>
                        <Select
                            defaultValue={this.state.analysisTags}
                            isMulti
                            name="analysisTags"
                            options={analysisTagOptions}
                            onChange={this.handleAnalysisSelectDropdownChange}
                            menuPlacement="auto"
                            menuPosition="fixed"
                        />
                    </label>
                    {sliders}
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
    analysisTagData: PropTypes.array,
    analysisTagMap: PropTypes.object,
    analysisValueRanges: PropTypes.array,
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
            analysisTagData: null,
            valueRanges: null,
        };
    }

    updateSearchData = (searchData) => {
        this.setState({ ...searchData });
    }

    async componentDidMount() {
        try {
            const searchTagResponse = await fetch('/api/get_tags/');
            const searchTags = await searchTagResponse.json();
            const {
                tags, photographers, analysisTags, valueRanges
            } = searchTags;
            // Sort by name and then by number, if the photographers have one
            photographers.sort((a, b) => {
                const aName = a.name;
                const bName = b.name;
                if (aName && bName) {
                    if (a.number && b.number) {
                        return aName.localeCompare(bName);
                    }
                    if (a.number) {
                        return -1;
                    }
                    if (b.number) {
                        return 1;
                    }
                    return aName.localeCompare(bName);
                }
                if (aName) {
                    return -1;
                }
                if (bName) {
                    return 1;
                }
                return 0;
            });
            this.setState({
                photographerData: photographers,
                tagData: tags,
                analysisTagData: analysisTags,
                valueRanges: valueRanges,
                loading: false,
            });
        } catch (e) {
            console.log(e);
        }
    }

    // This follows the full text + advanced search model here: http://photogrammar.yale.edu/search/
    render() {
        if (!this.state.tagData || !this.state.photographerData || !this.state.analysisTagData) {
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
                            analysisTagData={Object.keys(this.state.analysisTagData)}
                            analysisTagMap={this.state.analysisTagData}
                            analysisValueRanges={this.state.valueRanges}
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
