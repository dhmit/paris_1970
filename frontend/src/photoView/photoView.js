import React from 'react';
import Navbar from '../about/Navbar';
import { Footer } from '../UILibrary/components';


export class PhotoView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            photo_data: null,
            display_side: 'front',
        };
    }

    async componentDidMount() {
        try {
            const photoId = window.location.pathname.split('/')[2];
            const response = await fetch(`/api/photo/${photoId}/`);
            if (!response.ok) {
                this.setState({ loading: false });
            } else {
                const photo_data = await response.json();
                this.setState({ photo_data, loading: false });
            }
        } catch (e) {
            console.log(e);
        }
    }

     flipPhoto = () => {
         if (this.state.display_side === 'front') {
             this.setState({
                 display_side: 'back',
             });
         } else {
             this.setState({
                 display_side: 'front',
             });
         }
     };

     render() {
         if (this.state.loading) {
             return (<h1>
                Loading!
             </h1>);
         }
         if (!this.state.photo_data) {
             return (<h1>
                Photo with id {window.location.pathname.split('/')[2]} is not in database.
             </h1>);
         }
         const {
             title,
             alt,
             front_src,
             back_src,
         } = this.state.photo_data;

         let src = front_src;
         if (this.state.display_side === 'back') {
             src = back_src;
         }

         return (<>
             <Navbar />
             <div className="page row">
                 <div className='image-view col-12 col-lg-6'>
                     <h1>Photo Title: {title}</h1>
                     <img className='image-photo' src={src} alt={alt}/>
                     <br/>
                     <button onClick={() => this.flipPhoto()}> Flip photo </button>
                 </div>
                 <div className='image-info col-12 col-lg-6'>
                     <h3>
                        Photographer:
                         <h5>
                            None
                         </h5>
                     </h3>
                     <h3>
                        Categories
                         <h5>
                            None
                         </h5>
                     </h3>
                     <h3>
                        Whitespace
                         <h5>
                            None
                         </h5>
                     </h3>
                     <h3>
                        Sentiment analysis:
                         <h5>
                            None
                         </h5>
                     </h3>
                     <h3>
                        People detected:
                         <h5>
                            None
                         </h5>
                     </h3>
                     <h3>
                        Text detected:
                         <h5>
                            None
                         </h5>
                     </h3>
                     <h3>
                        Objects detected:
                         <h5>
                            None
                         </h5>
                     </h3>
                     <h3>
                        Map Square Information:
                         <h5>
                            None
                         </h5>
                     </h3>
                 </div>
             </div>
             <Footer />
         </>);
     }
}
