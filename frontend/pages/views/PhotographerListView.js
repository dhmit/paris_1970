import React from "react";
import Footer from "../../components/Footer";
import * as PropTypes from "prop-types";


export class PhotographerListView extends React.Component {
    constructor(props) {
        super(props);
    }

    hrefFunc (number) {
        return `/photographer/${number}`;
    };

    srcFunc (number) {
        return `${this.props.photoListDir}/${number}_photo.jpg`;
    };

    getPhotoList(){
         const photoSize = [100, 100];
         return this.props.photographers.map((photog,k) =>{
             return (
                 <>
                     <div className="col-2 col-lg-2 one-photographer">
                         <div className="child">
                             <a
                                key={k}
                                href={this.hrefFunc(photog[0])}
                             >
                                 <img
                                     alt={photog[0]}
                                     width={photoSize[0]}
                                     src={this.srcFunc(photog[0])}
                                 />
                             </a>
                             <p>{photog[1]? photog[1]:"No Name"}</p>
                         </div>
                     </div>
                 </>
             );
        });

    }

    render () {
        return (
            <>
                <div className="row">
                    <p style={{fontSize: "30px", fontWeight: "600"}}>Photographers</p>
                </div>
                <div className="row">
                    <>{this.getPhotoList()}</>
                </div>
                <div>
                    <Footer/>
                </div>
            </>
        );
    }
}


PhotographerListView.propTypes = {
    photoListDir: PropTypes.string,
    photographers: PropTypes.array
        };

