import React from "react";
import Footer from "../../components/Footer";
import * as PropTypes from "prop-types";



class DropDown extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            toggleDropDown: false,
            toggleDropDownItem: false,
            selected: null
        };
    }


    componentDidUpdate(prevState){
        if (this.state.toggleDropDown !== prevState.toggleDropDown || 
            this.state.toggleDropDownItem !== prevState.toggleDropDownItem) {
                let overlay = document.getElementsByClassName("overlay")[0];
        if (this.state.toggleDropDownItem || this.state.toggleDropDown) {
            overlay.classList.remove("hide");
            overlay.classList.add("show");
          } else {
            overlay.classList.remove("show");
            overlay.classList.add("hide");
          }
            }
    }

    render () {
        return(
           <div className="dropdown-container">
                <div className="dropdown-select"
                    style={{border:this.props.blue?"1px solid $color-turquoise":"1px solid #FB2F2A"}}
                    onMouseEnter={()=>{
                        this.setState({toggleDropDown:true});
                        let dropdowns = document.getElementsByClassName("dropdown-items");
                        for (const elt of dropdowns) {
                            if (elt.id !== this.props.id) {
                                elt.classList.add("d-none");
                            }
                        }
                    }}
                    onMouseLeave={()=>{
                        this.mouseLeaveTimer = setTimeout(()=>{
                            if (!this.state.toggleDropDownItem) {
                                this.setState({toggleDropDown:false});
                            }
                        }, 1000);
                    }}
                >
                    <p>{this.state.selected || this.props.placeholder}</p>
                    {/* TODO: add chevron down */}
                </div>
                <div className={`dropdown-items ${this.state.toggleDropDown?"":"d-none"}`} 
                id={this.props.id}>
                    {this.props.items.map((item)=>{
                        return(
                        <div key={item} 
                        className={`dropdown-itm ${this.state.selected === item ? "selected-itm": "unselected-itm"}`}
                        onClick={()=>{
                            if (this.state.selected !== item) {
                                this.setState({selected:item});
                            } else {
                                this.setState({selected:null});
                            }
                            
                        }}
                        onMouseEnter={()=>{
                            this.setState({
                                toggleDropDown:true,
                                toggleDropDownItem:true
                            });
                        }}
                        onMouseLeave={()=>{
                            this.setState({
                                toggleDropDown:false,
                                toggleDropDownItem:false
                            });
                        }}>{item}</div>);})}
                    
                       
                    
                </div>
           </div>
        );
    };
};

export class PhotographerListView extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            photographers: JSON.parse(this.props.photographers),
            timer: null
                };

        this.LOCATIONS = ["1", "2", "3"];
        this.SQUARES = ["4", "5", "6"];
        this.ALPHABET = ["7", "8", "9"];
        this.SORTS = ["10", "11", "12"];
   
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
    };


    handleScroll = () => {

        console.log("in handle nav");
        // Detecting scroll end adapted from https://stackoverflow.com/a/4620986
        if (this.scrollOverTimer !== null) {
          clearTimeout(this.scrollOverTimer);
        }

        let dropdowns = document.getElementsByClassName("dropdown-items");
        for (const elt of dropdowns) {
            elt.classList.add("d-none");
        };

        
        
        this.scrollOverTimer= setTimeout(() => {
            console.log("retract");
            // If the timer elapses, show to
            // this.setState({retract:true});
            document.getElementsByClassName("banner")[0].classList.add("grow");
            document.getElementsByClassName("banner")[0].classList.remove("shrink");


            }, 1000);

            document.getElementsByClassName("banner")[0].classList.add("shrink");
            document.getElementsByClassName("banner")[0].classList.remove("grow");  
        

            if (window.scrollY > 70) {
                document.getElementsByClassName("banner")[0].style.position = "fixed";
                document.getElementsByClassName("banner")[0].style.top = "0px";
            } else {
                document.getElementsByClassName("banner")[0].style.position = "absolute";
                document.getElementsByClassName("banner")[0].style.top = "70px";
            }
      };



    componentDidMount(){
        // if (!this.galleryRef) {
        //     return;
        //   }
        window.addEventListener("scroll", this.handleScroll);
    };

    componentWillUnmount(){
        window.removeEventListener("scroll", this.handleScroll);
    };
    

   
       
    

    render() {
        return (
            <>
                <div className="photographerList-container">
                <div className="overlay"></div>


                    <div className={"banner"}>
                        <p className="heading">Photographers</p>
                        <form className={"filterContainer"}>
                            {/* TODO: add magnify glass icon down */}
                                <input type="text" id="photographerList-search" placeholder="Search by name"/>
                                <div className="advancedSearch-container">
                                    <div className="filterBy-container">
                                        <p>Filter by:</p>
                                        <div style={{display:"flex", flexDirection:"row", columnGap:"5vw"}}>
                                            <DropDown id="loc-filter" blue={true} 
                                            items={this.LOCATIONS} placeholder={"Locations"}/>
                                            <DropDown id="sq-filter" blue={true} 
                                            items={this.SQUARES} placeholder={"Map Square"}/>
                                            <DropDown id="alph-filter" blue={true} 
                                            items={this.ALPHABET} placeholder={"Alphabet"}/>
                                        </div>
                                    </div>
                                    <div className="sortBy-container">
                                        <p>Sort by:</p>
                                        <DropDown id="sort" blue={false} items={this.SORTS} placeholder={"---"}/>
                                        
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

DropDown.propTypes = {
    id: PropTypes.string,
    blue: PropTypes.bool,
    items: PropTypes.array,
    placeholder: PropTypes.string
};

