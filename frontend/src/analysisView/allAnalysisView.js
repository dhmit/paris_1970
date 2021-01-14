import React from 'react';
import { Navbar, Footer } from '../UILibrary/components';

export class AllAnalysisView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: false,
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
        return (
            <>
                <Navbar />
                <div className='page'>
                    hi
                </div>
                <Footer />
            </>
        );
    }
}
