import React from 'react';
import Navbar from '../about/Navbar';
import { Footer } from '../UILibrary/components';

const SIDES = ['front', 'back', 'binder'];

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
                const photo_data = await response.json();
                const available_sides = SIDES.filter((side) => photo_data[`${side}_src`] !== '');
                const display_side = available_sides.length > 0 ? available_sides[0] : '';
                this.setState({
                    photo_data,
                    available_sides,
                    display_side,
                    loading: false,
                });
            }
        } catch (e) {
            console.log(e);
        }
    }

    changeSide = (display_side) => {
        this.setState({ display_side });
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
                        return (<></>);
                    })}

                </div>
                <div className='image-info col-12 col-lg-6'>
                    <h3>
                        Photographer:
                        <h5>
                            None
                        </h5>
                    </h3>
                    <h3>
                        Categories
                        <h5>
                          None
                        </h5>
                    </h3>
                    <h3>
                        Whitespace
                        <h5>
                            None
                        </h5>
                    </h3>
                    <h3>
                        Sentiment analysis:
                        <h5>
                            None
                        </h5>
                    </h3>
                    <h3>
                        People detected:
                        <h5>
                            None
                        </h5>
                    </h3>
                    <h3>
                        Text detected:
                        <h5>
                            None
                        </h5>
                    </h3>
                    <h3>
                        Objects detected:
                        <h5>
                            None
                        </h5>
                    </h3>
                    <h3>
                        Map Square Information:
                        <h5>
                            None
                        </h5>
                    </h3>
                </div>
            </div>
            <Footer />
        </>);
    }
}
