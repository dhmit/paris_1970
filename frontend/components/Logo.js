// import React from "react";
// import ReactDOM from "react-dom";
// import * as PropTypes from "prop-types";

// export class Logo extends React.Component {
//     constructor(props) {
//         super(props);

//         //Positions in terms of %
//         this.top = props.top;
//         this.left = props.left;
//         //Position anchor (relative, absolute, etc)
//         this.position_type = props.position;
//         //For identifying css styling. Check logo.scss for valid inputs
//         this.logo_type = props.logo_type;

//     }

//     render() {
//         return (
//             //All logos can consist of a red square and/or a blue square. They are contained
//             //within a parent div/bounding box
//             <div className={"parent-bounding-box-"+this.logo_type} style={{top: this.top+"%",
//                                                          left: this.left+"%",
//                                                          position:this.position_type}}>
//                 <div className={"red-rectangle-"+this.logo_type}/>
//                 <div className={"blue-rectangle-"+this.logo_type}/>
//             </div>
//         );
//     }
// }

// Logo.propTypes = {
//     top: PropTypes.number,
//     left: PropTypes.number,
//     position: PropTypes.string,
//     logo_type: PropTypes.string
// };

// Logo.defaultProps = {
//     top: 0,
//     left: 0,
//     position: "relative"
// };

// export default Logo;
// ReactDOM.render(<Logo/>, document.getElementById("logo"));


