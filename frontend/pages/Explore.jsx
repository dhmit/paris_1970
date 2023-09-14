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
            isLoading: false,
            currentPage: 1,
            desiredPage: 1,
            totalPages: -1,
            totalCount: -1,
            pageSize: 10,
        };
    }

    handleChangeTags = (event) => {
        this.setState({ selectedTag: event.target.value }, this.fetchData);
    };

    handlePageSizeChange = (size) => {
        this.setState({ pageSize: size }, this.fetchData);
    };

    handleDesiredPageChange = (event) => {
        this.setState({ desiredPage: event.target.value });
    };

    handleGoToPage = () => {
        const { desiredPage, totalPages } = this.state;
        if (desiredPage >= 1 && desiredPage <= totalPages) {
            this.setState({ currentPage: desiredPage }, this.fetchData);
        } else {
            console.warn('Desired page out of range');
        }
    };

    fetchData = async () => {
        this.setState({ isLoading: true });
        console.log('fetching page', this.state.currentPage);

        try {
            const response = await fetch('/api/explore/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    selectedTag: this.state.selectedTag,
                    page: this.state.currentPage,
                    pageSize: this.state.pageSize,
                })
            });

            const data = await response.json();
            console.log(data);
            this.setState({
                photos: data.photos,
                totalCount: data.totalCount,
                totalPages: data.totalPages,
                isLoading: false
            });

        } catch (e) {
            console.log(e);
            this.setState({ isLoading: false });
        }
    };

    componentDidMount = async () => {
        this.fetchData();
    };

    handlePageChange(direction) {
        if (direction === 'next') {
            this.setState(prevState => ({ currentPage: prevState.currentPage + 1 }), this.fetchData);
        } else if (direction === 'previous') {
            this.setState(prevState => ({ currentPage: prevState.currentPage - 1 }), this.fetchData);
        }
    }

    hasPreviousPage() { return this.state.currentPage > 1; }

    hasNextPage() { return this.state.currentPage < this.state.totalPages; }

    render() {
        const { objects } = this.props;
        const { selectedTag, photos, isLoading, currentPage, totalCount, pageSize } = this.state;
        const totalPages = Math.ceil(totalCount / pageSize);

        const startImage = (currentPage - 1) * pageSize + 1;
        const endImage = Math.min(currentPage * pageSize, totalCount); // Using min to ensure we don't exceed totalCount

        const paginationControls = (
            <div className="pagination-controls d-flex justify-content-between align-items-center">
                {this.hasPreviousPage()
                    ? <button className="btn btn-primary" onClick={() => this.handlePageChange('previous')}>Previous Page</button>
                    : <div></div>
                }
                <div className="text-center">
                    <p>
                        Page {currentPage} of {totalPages}<br/>
                        Showing Photos {startImage} - {endImage} out of {totalCount}
                    </p>
                    <div className="d-flex align-items-center justify-content-center">
                        <label>Go to Page: </label>
                        <input
                            type="number"
                            className="form-control mx-4"
                            value={this.state.desiredPage}
                            onChange={this.handleDesiredPageChange}
                            style={{ width: '60px' }}
                        />
                        <button className="btn btn-secondary ml-2" onClick={this.handleGoToPage}>Go</button>
                    </div>
                </div>
                {this.hasNextPage() &&
                    <button className="btn btn-primary" onClick={() => this.handlePageChange('next')}>Next Page</button>
                }
            </div>
        );


        return (
            <section className="explore">
                <div className="row gx-0">
                    <div className="sidebar-container col-4">
                        <div className="sidebar" style={{backgroundImage: `url(${SearchBgTopLeft})`, backgroundPosition: 'top left', backgroundRepeat: 'no-repeat'}}>
                            <div className="form-group mb-2">
                                <label htmlFor="formTags">Objects</label>
                                <select className="form-control" value={selectedTag} onChange={this.handleChangeTags}>
                                    <option key="All">All</option>
                                    {objects.map(tag => <option key={tag}>{tag}</option>)}
                                </select>
                            </div>

                            <div className="form-group mb-2">
                                <label>Images per Page</label>
                                <div>
                                    <button className={`btn ${this.state.pageSize === 10 ? 'btn-primary' : 'btn-light'}`} onClick={() => this.handlePageSizeChange(10)}>10</button>
                                    <button className={`btn ml-2 ${this.state.pageSize === 25 ? 'btn-primary' : 'btn-light'}`} onClick={() => this.handlePageSizeChange(25)}>25</button>
                                    <button className={`btn ml-2 ${this.state.pageSize === 50 ? 'btn-primary' : 'btn-light'}`} onClick={() => this.handlePageSizeChange(50)}>50</button>
                                </div>
                            </div>

                            <p className="explainer">
                            Use these tools to sort photos according to subjects and location. The object detection tool uses
                            the YOLO (You Only Look Once) algorithm. Click on any photo to view it and its metadata,
                            where you will also find a gateway to the similarity algorithm.
                            </p>
                        </div>
                    </div>
                    <div className="photos col-8">
                        {isLoading ? (
                            <Loading />
                        ) : (<>
                            {paginationControls}
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
                            {paginationControls}
                        </>)}
                    </div>
                </div>
            </section>
        );
    }
}

export default Explore;
