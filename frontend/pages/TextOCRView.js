import React from "react";

import PhotoViewer from "../../components/PhotoViewer";
import LoadingPage from "../LoadingPage";


export class TextOCRView extends PhotoViewer {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photoData: null
        };
    }

    async componentDidMount() {
        try {
            const response = await fetch("/api/text_ocr/");
            if (!response.ok) {
                this.setState({loading: false});
            } else {
                const photoData = await response.json();
                console.log(photoData);
                this.setState({
                    photoData,
                    loading: false
                });
            }
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        if (this.state.loading) return (<LoadingPage/>);

        return (<>
            <div className="page">
                <h1 className="mb-4">Photos that maybe have text in them</h1>
                <ul className={"list-inline"}>
                    {this.state.photoData.map((photo, key) => <>
                        <li className={"default-photo photo-item-background text-center list-inline-item"}
                            key={key}
                            style={{"width": 400, "height": 400}}
                        >
                            <a href={photo.photo_page_url}>
                                <figure>
                                    <img alt={photo.alt} 
                                         style={{maxWidth: 400, maxHeight: 400}} 
                                         src={photo.photo_url} />
                                    <figcaption>
                                        {photo.text}
                                    </figcaption>
                                </figure>
                            </a>
                        </li>
                    </>)}
                </ul>
            </div>
        </>);
    }
}
