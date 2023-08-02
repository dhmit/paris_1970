import React from 'react';

import SearchBgTopLeft from "../images/search_top_left.svg";
import SearchBgTopRight from "../images/search_top_right.svg";

interface Photo {
    number: number;
    map_square_number: number;
    folder: string;
    photographer_number: number;
    photographer_name: string;
    photo_url: string;
    photo_page_url: string;
}

interface ExploreProps {
    readonly objects: string[];
    readonly arrondissements: number[];
}

interface ExploreState {
    selectedTag: string;
    selectedMapSquare: number;
    photos: Photo[];
}

export class Explore extends React.Component<ExploreProps, ExploreState> {
    constructor(props: ExploreProps) {
        super(props);
        this.state = {
            selectedTag: "",
            selectedMapSquare: 0,
            photos: [],
        };
    }

    handleChangeTags = (event: React.ChangeEvent<HTMLSelectElement>) => {
        this.setState({ selectedTag: event.target.value }, this.fetchData);
    };

    handleChangeMapSquares = (event: React.ChangeEvent<HTMLSelectElement>) => {
        this.setState({ selectedMapSquare: Number(event.target.value) }, this.fetchData);
    };

    fetchData = async () => {
        try {
            const response = await fetch('/api/explore/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    selectedTag: this.state.selectedTag,
                    selectedMapSquare: this.state.selectedMapSquare
                })
            });

            const data = await response.json();
            this.setState({ photos: data.photos });
        } catch (e) {
            console.log(e);
        }
    };

    render() {
        const { objects, arrondissements } = this.props;
        const { selectedTag, selectedMapSquare, photos } = this.state;

        return (
            <>
                <div className="row">
                    <div className="col-3">
                        <SearchBgTopLeft className="search-bg-image-left"/>
                        <SearchBgTopRight className="search-bg-image-right"/>
                        <div className="sidebar">
                            <div className="form-group">
                                <label htmlFor="formTags">Select Tag</label>
                                <select className="form-control" value={selectedTag} onChange={this.handleChangeTags}>
                                    {objects.map(tag => <option key={tag}>{tag}</option>)}
                                </select>
                            </div>

                            <div className="form-group">
                                <label htmlFor="formMapSquares">Select Map Square</label>
                                <select className="form-control" value={selectedMapSquare} onChange={this.handleChangeMapSquares}>
                                    {arrondissements.map(arr => <option key={arr} value={arr}>Arrondissement {arr}</option>)}
                                </select>
                            </div>
                        </div>
                    </div>
                    <div className="col-9">
                        <div className="row">
                            {photos.length > 0 && photos.map(photo => (
                                <div className="col-4" key={photo.number}>
                                    <a href={photo.photo_page_url}>
                                        <div className="card mb-4">
                                            <img className="card-img-top" src={photo.photo_url} alt={photo.number.toString()} />
                                            <div className="card-body">
                                                <h5 className="card-title">Photo {photo.number}</h5>
                                                <p className="card-text">Photographer: {photo.photographer_name}</p>
                                            </div>
                                        </div>
                                    </a>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </>
        );
    }

}

export default Explore;
