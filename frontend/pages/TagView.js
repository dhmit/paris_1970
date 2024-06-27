import React from "react";
import ParisMap, {MAPSQUARE_HEIGHT, MAPSQUARE_WIDTH} from "../components/ParisMap";
import * as PropTypes from "prop-types";
import PhotoViewer from "../components/PhotoViewer";
import LoadingPage from "./LoadingPage";
import { MapSquareViewer, arrondissementsOverlay } from "./MapPageView";
import { Popup, Rectangle } from "react-leaflet";
import { Trans, withTranslation } from "react-i18next";

function densityOverlay(mapSquareData, translator) {
    const sortedMapData = Object.values(mapSquareData)
    .sort((a, b) => a.num_photos - b.num_photos);
    // Gets the max number of photos in a single square out of all squares to form buckets later
    const maxNumOfPhotos = sortedMapData && sortedMapData.length
        ? sortedMapData[sortedMapData.length - 1].num_photos
        : 0;
    // Creating 5 buckets based on lowest to highest number of photos per square
    const twentyPctMax = Math.round(0.2 * maxNumOfPhotos);
    const fortyPctMax = Math.round(0.4 * maxNumOfPhotos);
    const sixtyPctMax = Math.round(0.6 * maxNumOfPhotos);
    const eightyPctMax = Math.round(0.8 * maxNumOfPhotos);
    return (<>
        {
            sortedMapData.map((mapSquareData) => {
                const index = mapSquareData.number;
                const coords = mapSquareData.topLeftCoords;
                const numberOfPhotos = mapSquareData.num_photos;

                const mapSquareBounds = [
                    [coords.lat, coords.lng],
                    [coords.lat - MAPSQUARE_HEIGHT, coords.lng - MAPSQUARE_WIDTH]
                ];
                const link = "/map_square/" + index;
                let mapSquareBucket = "";
                // set of conditionals to calculate photo density for heat map
                if (numberOfPhotos > 0 && numberOfPhotos <= twentyPctMax) {
                    mapSquareBucket = "map-square box-one";
                } else if (numberOfPhotos <= fortyPctMax) {
                    mapSquareBucket = "map-square box-two";
                } else if (numberOfPhotos <= sixtyPctMax) {
                    mapSquareBucket = "map-square box-three";
                } else if (numberOfPhotos <= eightyPctMax) {
                    mapSquareBucket = "map-square box-four";
                } else if (numberOfPhotos <= maxNumOfPhotos) {
                    mapSquareBucket = "map-square box-five";
                }

                return (
                    <Rectangle
                        className={numberOfPhotos === 0 ? "map-grid" : mapSquareBucket}
                        key={index}
                        bounds={mapSquareBounds}>
                        <Popup>
                            {translator("global.mapSquare")} {index} <br/>
                            <a href={link}>{numberOfPhotos} {translator("global.photos")}</a>
                        </Popup>
                    </Rectangle>
                );
            })
        }
    </>);
}


function Mix(bases) {
    // https://stackoverflow.com/a/61860802
    class Bases extends React.Component {
        constructor(props) {
            super(props);
            bases.forEach(base => Object.assign(this, new base()));
            this.props = props;
        }
    }
    
    bases.forEach(base => {
        Object.getOwnPropertyNames(base.prototype)
        .filter(prop => prop !== 'constructor')
        .forEach(prop => Bases.prototype[prop] = base.prototype[prop]);
    });
    return Bases;
}


class BaseTagView extends Mix([PhotoViewer, MapSquareViewer]) {
    constructor(props) {
        super(props);

        this.state = {
            mapData: null,
            geojsonData: null,
            filledMapSquares: null,
            filledMapSquaresData: null,
            isLgViewportUp: null,
            mapSquare: null,
            photos: JSON.parse(this.props.tagPhotos),
            photographers: []
        };
    }

    async componentDidMount() {
        await this.getMapData();
        try {
            const geojsonResponse = await fetch("/api/arrondissements_geojson/");
            const geojsonData = await geojsonResponse.json();

            //Makes a set of all map squares with num_photos equal to the number of pictures for the current tag
            const filledMapSquares = new Set();
            const filledMapSquaresData = {};
            for (const photo of this.state.photos) {
                console.log("photo: ", photo);
                const photoMapSquare = this.state.mapData[photo["map_square_number"]];
                const photoMapSquareNumber = photo["map_square_number"];
                filledMapSquares.add(photoMapSquare["id"]);
                if (!filledMapSquaresData[photoMapSquareNumber]) {
                    filledMapSquaresData[photoMapSquareNumber] = photoMapSquare;
                    filledMapSquaresData[photoMapSquareNumber].num_photos = 0;
                }
                filledMapSquaresData[photoMapSquareNumber].num_photos += 1;
            }
            for (const mapSquare of Object.values(this.state.mapData)) {
                if (!filledMapSquaresData[mapSquare["id"]]) {
                    filledMapSquaresData[mapSquare["id"]] = mapSquare;
                    filledMapSquaresData[mapSquare["id"]].num_photos = 0;
                }
            }
            this.setState({
                filledMapSquares: filledMapSquares,
                filledMapSquaresData: filledMapSquaresData,
                geojsonData: geojsonData["features"],
                loading: false
            });
        } catch (e) {
            console.log(e);
        }
    }

    render() {

        if (this.props.tagPhotos.length === 0) {
            return <Trans
                i18nKey="TagView.tagNotFound"
                values={{ tagName: this.props.tagName }}
            />;
        }
        const tag = this.props.tagName;
        const photos = JSON.parse(this.props.tagPhotos);

        if (!this.state.mapData || !this.state.filledMapSquares || !this.state.filledMapSquaresData) {
            return <LoadingPage/>;
        }
        const arrondissementLabel = this.props.t("global.arrondissement");
        const photosAvailableLabel = this.props.t("global.photosAvailable");
        const mapLayers = {};
        mapLayers[arrondissementLabel] = arrondissementsOverlay(this.state.geojsonData);
        mapLayers[photosAvailableLabel] = densityOverlay(this.state.filledMapSquaresData, this.props.t);    
        return (<>
            <div className="row">
                <div className="tag-info col-12 col-lg-5">
                    <p className="tag-header">{this.props.t("TagView.tagHeader")}</p>
                    <p className="tag-title">{tag}</p>
                    <p><Trans
                        i18nKey="TagView.numResults"
                        values={{ numResults: this.props.totalNumPhotos }}
                    /></p>
                    <p><Trans
                        i18nKey="TagView.pageIndicator"
                        values={{ currentPage: this.props.pageNum, totalPages: this.props.numPages }}
                    /></p>
                    <ul className="p-0">{this.getPhotoGrid(photos, {"photoSize": [120, 120]})}</ul>
                </div>
                <div className="tag-map col-12 col-lg-7">
                    <ParisMap
                        className="tags-map"
                        zoom={14}
                        layers={mapLayers}
                        visibleLayers={Object.keys(mapLayers)} 
                        layerSelectVisible={true}
                        t={this.props.t}
                    />
                </div>
            </div>
        </>);
    }
}

BaseTagView.propTypes = {
    tagName: PropTypes.string,
    tagPhotos: PropTypes.string,
    totalNumPhotos: PropTypes.number,
    pageNum: PropTypes.number,
    numPages: PropTypes.number,
};

const TagView = withTranslation()(BaseTagView);
export default TagView;
