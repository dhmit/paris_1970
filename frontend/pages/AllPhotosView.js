import React from "react";

import Footer from "../components/Footer";
import PhotoViewer from "../components/PhotoViewer";
import LoadingPage from "./LoadingPage";


export class AllPhotosView extends PhotoViewer {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photoData: null,
            displayOrder: "Ascending"
        };
    }

    async componentDidMount() {
        try {
            const apiURL = "/api/all_photos";
            const response = await fetch(apiURL);
            if (!response.ok) {
                this.setState({loading: false});
            } else {
                const photoData = await response.json();
                this.setState({
                    photoData,
                    loading: false
                });
            }
        } catch (e) {
            console.log(e);
        }
    }

    reverseOrder = () => {
        let newOrder;
        if (this.state.displayOrder === "Descending") {
            newOrder = "Ascending";
        } else {
            newOrder = "Descending";
        }
        const newPhotoData = this.state.photoData.reverse();
        this.setState({
            photoData: newPhotoData,
            displayOrder: newOrder
        });
    };

    render() {
        if (this.state.loading) {
            return (<LoadingPage/>);
        }

        const hrefFunc = (_key, photo) => `/similar_photos/${photo.map_square_number}/` +
                                       `${photo.folder_number}/${photo.number}/10/`;

        const photos = this.getPhotoGrid(this.state.photoData, {"hrefFunc": hrefFunc});

        const options = this.state.photoData.length === 0 ? (
            <p>
                {"There are no photos that have an analysis result for resnet18_cosine_similarity" +
                " or the analysis does not exist."}
            </p>) : (<div className="options">
            <p>Click on a photo to see the 10 most similar matches!</p></div>);

        return (<>
            <div className="display-box page">
                <h3 className="text-capitalize">
                    {"resnet18_cosine_similarity"}
                </h3>
                {options}
                <br/>
                {photos}
            </div>
            <Footer/>
        </>);
    }
}
