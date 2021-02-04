import React from 'react';
import { Navbar, Footer } from '../UILibrary/components';

export const analysisDescriptions = {
    whitespace_percentage: {
        name: 'Whitespace Percentage',
        desc: 'This analysis gives a number between 0 and 100, which is the percentage'
              + ' of the photo that is made up of whitespace.',
    },
    photographer_caption_length: {
        name: 'Photograph Caption Length',
        desc: 'This analysis gives the number of characters in the caption of the photo',
    },
    mean_detail: {
        name: 'Mean Detail',
        desc: 'This analysis gives a number to represent what the mean detail in a photo is.',
    },
    portrait_detection: {
        name: 'Portrait Detection',
        desc: 'This analysis tells you whether the photo is a portrait or not.',
    },
    foreground_percentage: {
        name: 'Foreground Percentage',
        desc: 'This analysis gives a number to represent what percentage of the image is the'
               + ' foreground.',
    },
    text_ocr: {
        name: 'Text Detected',
        desc: 'This analysis attempts to recognize the text in an image using the OpenCV East'
               + ' text detector and Tesseract OCR.',
    },
    yolo_model: {
        name: 'Yolo Model',
        desc: 'This analysis detects objects in a photo using the YOLO model.',
    },
    find_vanishing_point: {
        name: 'Vanishing Point and Significant Lines',
        desc: 'This analysis detects significant lines and if a photo has a vanishing point.',
    },
};

export class AllAnalysisView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            analysisData: null,
        };
    }

    async componentDidMount() {
        try {
            const apiURL = '/api/all_analyses';
            const response = await fetch(apiURL);
            if (!response.ok) {
                this.setState({ loading: false });
            } else {
                const analysisData = await response.json();
                this.setState({
                    analysisData,
                    loading: false,
                });
            }
        } catch (e) {
            console.log(e);
        }
    }


    render() {
        if (this.state.loading) {
            return (<h1>
                Loading!
            </h1>);
        }

        const analysisDivs = [];
        this.state.analysisData.forEach((analysis) => {
            if (analysisDescriptions[analysis].name !== undefined) {
                const div = (
                    <div key={analysis}>
                        <h2><a className='analysis-link' href={`/analysis/${analysis}/`}>
                            {analysisDescriptions[analysis].name}
                        </a></h2>
                        <p>{analysisDescriptions[analysis].desc}</p>
                    </div>
                );
                analysisDivs.push(div);
            }
        });

        return (
            <>
                <Navbar />
                <div className='page'>
                    <h1 className='pb-2'>All Analysis Results</h1>
                    {analysisDivs}
                </div>
                <Footer />
            </>
        );
    }
}
