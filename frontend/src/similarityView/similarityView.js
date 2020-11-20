import React from 'react';
import * as PropTypes from 'prop-types';

import Navbar from '../about/navbar';
import { Footer } from '../UILibrary/components';

const SIDES = {
    CLEANED: 'cleaned',
    FRONT: 'front',
    BACK: 'back',
    BINDER: 'binder',
};

export class SimilarityView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photoData: null,
        };
    }

    async componentDidMount() {
        try {
            // eslint-disable-next-line
            // eslint-disable-next-line max-len
            const apiURL = `/api/similar_photos/${this.props.mapSquareNumber}/${this.props.photoNumber}/`;
            const response = await fetch(apiURL);
            if (!response.ok) {
                this.setState({ loading: false });
            } else {
                const photoData = await response.json();
                this.setState({ photoData, loading: false });
            }
        } catch (e) {
            console.log(e);
        }
    }

    /* changeSide = (displaySide) => {
        this.setState({ displaySide: displaySide });
    }; */

    getSource(photoData) {
        const availableSides = Object.values(SIDES).filter(
            (side) => photoData[`${side}_src`] !== null,
        );
        const displaySide = availableSides.length > 0 ? availableSides[0] : '';
        const source = photoData[`${displaySide}_src`];
        return source;
    }

    // eslint-disable-next-line consistent-return
    render() {
        if (this.state.loading) {
            return (<h1>
                Loading!
            </h1>);
        }

        if (!this.state.photoData) {
            return (<h1>
                Photo with id {window.location.pathname.split('/')[2]} is not in database.
            </h1>);
        }
        const photos = this.state.photoData.map((photo, k) => {
            return (
                <a
                    key={k}
                    // title={currentAnalysis.result}
                    href={`/photo/${photo['map_square_number']}/${photo['number']}/`}
                >
                    <img
                        alt={photo.alt}
                        height={200}
                        width={200}
                        src={this.getSource(photo)}
                    />
                </a>
            );
        });



        return (<>
            <Navbar />
            <div className="page row">
                <div className='image-info col-12 col-lg-8'>
                    {/* {similarPhotos.map((photo, k) => ( */}
                    {/*    <a */}
                    {/*        key={k} */}
                    {/*        href={`/photo/${photo['map_square_number']}/${photo['number']}/`} */}
                    {/*    > */}
                    {/*        <img */}
                    {/*            alt={photo.alt} */}
                    {/*            height={100} */}
                    {/*            width={100} */}
                    {/*            src={this.getSource(photo)} */}
                    {/*        /> */}
                    {/*    </a> */}
                    {/* ))}  */}
                    {photos}
                </div>
            </div>
            <Footer />
        </>);
    }
}
SimilarityView.propTypes = {
    photoNumber: PropTypes.number,
    mapSquareNumber: PropTypes.number,
};
