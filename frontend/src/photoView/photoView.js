import React from 'react';
import Navbar from '../about/navbar';
import { Footer } from '../UILibrary/components';

const SIDES = {
    FRONT: 'front',
    BACK: 'back',
    BINDER: 'binder',
};

const ATTRIBUTES_TO_DISPLAY_NAME = {
    white_space_ratio_back: 'White Space Ratio of Back Side',
    white_space_ratio_front: 'White Space Ratio of Front Side',
    white_space_ratio_binder: 'White Space Ratio of Binder Side',
};

export class PhotoView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photo_data: null,
            display_side: '',
            available_sides: [],
        };
    }

    async componentDidMount() {
        try {
            const photoId = window.location.pathname.split('/')[2];
            const response = await fetch(`/api/photo/${photoId}/`);
            if (!response.ok) {
                this.setState({ loading: false });
            } else {
                const photoData = await response.json();
                const availableSides = Object.values(SIDES)
                    .filter((side) => photoData[`${side}_src`] !== '');
                const displaySide = availableSides.length > 0 ? availableSides[0] : '';
                this.setState({
                    photo_data: photoData,
                    available_sides: availableSides,
                    display_side: displaySide,
                    loading: false,
                });
            }
        } catch (e) {
            console.log(e);
        }
    }

    changeSide = (displaySide) => {
        this.setState({ display_side: displaySide });
    };

    render() {
        if (this.state.loading) {
            return (<h1>
                Loading!
            </h1>);
        }
        if (!this.state.photo_data) {
            return (<h1>
                Photo with id {window.location.pathname.split('/')[2]} is not in database.
            </h1>);
        }
        const {
            title,
            alt,
        } = this.state.photo_data;

        return (<>
            <Navbar />
            <div className="page row">
                <div className='image-view col-12 col-lg-6'>
                    <h1>Photo Title: {title}</h1>
                    <img
                        className='image-photo'
                        src={this.state.photo_data[`${this.state.display_side}_src`]}
                        alt={alt}
                    />
                    <br/>
                    {this.state.available_sides.map((side, k) => {
                        if (side !== this.state.display_side) {
                            return (
                                <button key={k} onClick={() => this.changeSide(side)}>
                                    {side[0].toUpperCase() + side.slice(1)} Side
                                </button>
                            );
                        }
                        return '';
                    })}

                </div>
                <div className='image-info col-12 col-lg-6'>
                    <h3>
                        Photographer:
                    </h3>
                    <h5>
                        None
                    </h5>
                    <h3>
                        Categories
                    </h3>
                    <h5>
                      None
                    </h5>
                    <h3>
                        Whitespace
                    </h3>
                    <h5>
                        None
                    </h5>
                    <h3>
                        Sentiment analysis:
                    </h3>
                    <h5>
                        None
                    </h5>
                    <h3>
                        People detected:
                    </h3>
                    <h5>
                        None
                    </h5>
                    <h3>
                        Text detected:
                    </h3>
                    <h5>
                        None
                    </h5>
                    <h3>
                        Objects detected:
                    </h3>
                    <h5>
                        None
                    </h5>
                    <h3>
                        Map Square Information:
                    </h3>
                    <h5>
                        None
                    </h5>
                    {Object.keys(ATTRIBUTES_TO_DISPLAY_NAME).map((attribute, k) => {
                        const attributeValue = this.state.photo_data[attribute];
                        if (attributeValue) {
                            return (
                                <div key={k}>
                                    <h3>{ATTRIBUTES_TO_DISPLAY_NAME[attribute]}:</h3>
                                    <h5>{attributeValue}</h5>
                                </div>
                            );
                        }
                        return '';
                    })}
                </div>
            </div>
            <Footer />
        </>);
    }
}
