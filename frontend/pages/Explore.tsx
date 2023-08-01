import React from "react";

interface ExploreViewProps {
    arrondissements: number[];
}

export class ExploreView extends React.Component {
    constructor(props: ExploreViewProps) {
        super(props);
        this.state = {
            loading: true,
            mapSquareData: null
        };
    }

    async componentDidMount() {
        try {
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        return (<>
            <div className="page">
            </div>
        </>);
    }
}
