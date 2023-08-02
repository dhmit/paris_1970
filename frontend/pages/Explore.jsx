import React from 'react';

import SearchBgTopLeft from "../images/search_top_left.svg?url";
import SearchBgTopRight from "../images/search_top_right.svg?url";
import Loading from '../components/Loading';

export class Explore extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedTag: "All",
            selectedMapSquare: "All",
            photos: [],
            isLoading: false
        };
    }

    handleChangeTags = (event) => {
        this.setState({ selectedTag: event.target.value }, this.fetchData);
    };

    handleChangeMapSquares = (event) => {
        this.setState({ selectedMapSquare: event.target.value }, this.fetchData);
    };

    fetchData = async () => {
        this.setState({ isLoading: true });

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
            this.setState({ photos: data.photos, isLoading: false });
        } catch (e) {
            console.log(e);
            this.setState({ isLoading: false });
        }
    };

    componentDidMount = async () => {
        this.fetchData();
    };

    render() {
        const { objects, arrondissements } = this.props;
        const { selectedTag, selectedMapSquare, photos, isLoading } = this.state;

        return (
            <section className="explore">
                <div className="row">
                    <div className="sidebar-container col-4">
                        <div className="sidebar" style={{backgroundImage: `url(${SearchBgTopLeft})`, backgroundPosition: 'top left', backgroundRepeat: 'no-repeat'}}>
                            <div className="form-group mb-2">
                                <label htmlFor="formTags">Objects</label>
                                <select className="form-control" value={selectedTag} onChange={this.handleChangeTags}>
                                    <option key="All">All</option>
                                    {objects.map(tag => <option key={tag}>{tag}</option>)}
                                </select>
                            </div>

                            <div className="form-group">
                                <label htmlFor="formMapSquares">Arrondissement</label>
                                <select className="form-control" value={selectedMapSquare} onChange={this.handleChangeMapSquares}>
                                    <option key="All" value="All">All</option>
                                    {arrondissements.map(arr => <option key={arr} value={arr}>{arr}</option>)}
                                </select>
                            </div>
                        </div>
                    </div>
                    <div className="photos col-8 p-5" style={{backgroundImage: `url(${SearchBgTopRight})`, backgroundPosition: 'top right', backgroundRepeat: 'no-repeat'}}>
                        {isLoading ? (
                            <Loading />
                        ) : (
                            <div className="row">
                                {photos.length > 0 && photos.map(photo => (
                                    <div className="col-4" key={photo.id}>
                                        <a href={photo.photo_page_url}>
                                            <div className="card mb-4">
                                                <img className="card-img-top" src={photo.photo_url} alt={photo.number.toString()} />
                                                <div className="card-body">
                                                </div>
                                            </div>
                                        </a>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </section>
        );
    }
}

export default Explore;
