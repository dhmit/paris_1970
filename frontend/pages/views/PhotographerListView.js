import React from "react";
import Footer from "../../components/Footer";
import * as PropTypes from "prop-types";


export class PhotographerListView extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            photographers: JSON.parse(this.props.photographers),
            timer: null
                };
            
    }

    hrefFunc(number) {
        return `/photographer/${number}`;
    };

    srcFunc(number) {
        return `${this.props.photoListDir}/${number}_photo.jpg`;
    };

    getPhotoList() {
        const photoSize = [100, 100];
        return this.state.photographers.map((photog, k) => {
            return (
                <li className="col-2 col-lg-2 one-photographer list-inline-item" key={k}>
                    <div className="child">
                        <a key={k}
                           href={this.hrefFunc(photog.number)}>
                            <img
                                alt={photog.number}
                                width={photoSize[0]}
                                src={this.srcFunc(photog.number)}/>
                        </a>
                        <p>{photog.name ? photog.name : "No Name"}</p>
                    </div>
                </li>
            );
        });
    }


    handleScroll = () => {

        console.log("in handle nav");
        // Detecting scroll end adapted from https://stackoverflow.com/a/4620986
        if (this.scrollOverTimer !== null) {
          clearTimeout(this.scrollOverTimer);
        }
    
        
        this.scrollOverTimer= setTimeout(() => {
            console.log("retract");
            // If the timer elapses, show to
            // this.setState({retract:true});
            document.getElementsByClassName("banner")[0].classList.add("grow");
            document.getElementsByClassName("banner")[0].classList.remove("shrink");

            // document.getElementsByClassName("filterContainer")[0].classList.add("grow");
            // document.getElementsByClassName("filterContainer")[0].classList.remove("shrink");
            }, 1000);

            document.getElementsByClassName("banner")[0].classList.add("shrink");
            document.getElementsByClassName("banner")[0].classList.remove("grow");   


            // document.getElementsByClassName("filterContainer")[0].classList.add("shrink");
            // document.getElementsByClassName("filterContainer")[0].classList.remove("grow");


        
      };



    componentDidMount(){
        // if (!this.galleryRef) {
        //     return;
        //   }
        window.addEventListener("scroll", this.handleScroll);
    }

    componentWillUnmount(){
        window.removeEventListener("scroll", this.handleScroll);
    }
    
       
    

    render() {
        return (
            <>
                <div className="photographerList-container">

                    <div className={"banner"}>
                        <p className="heading">Photographers</p>
                        <form className={"filterContainer"}>
                                <input type="text" id="photographerList-search" placeholder="Search by name"/>
                                <div className="advancedSearch-container">
                                    <div className="filterBy-container">
                                        <p>Filter by:</p>
                                        

                                    
                                        
                                    </div>
                                    <div className="sortBy-container">
                                        <p>Sort by:</p>
                                        
                                    </div>
                                    
                                </div>

                        </form>
                    </div>

                    <div className="photographerGallery">
                        {/* <ul className="list-inline">{this.getPhotoList()}</ul> */}
                    </div>
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
    photographers: PropTypes.string
};

