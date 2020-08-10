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
             return (<>
                Loading!
             </>);
         }
         if (!this.state.photo_data) {
             return (<>
                Photo with id {window.location.pathname.split('/')[2]} is not in database.
             </>);
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
                     <h2>Photo Title: {title}</h2>
                     <img className='image-photo' src={src} alt={alt}/>
                     <br/>
                     <button onClick={() => this.flipPhoto()}> Flip photo </button>
                 </div>
                 <div className='image-info col-12 col-lg-6'>
                     <div className='attribute-title'>
                        Photographer:
                         <div className='attribute'>
                            None
                         </div>
                     </div>
                     <div className='attribute-title'>
                        Categories
                         <div className='attribute'>
                            None
                         </div>
                     </div>
                     <div className='attribute-title'>
                        Whitespace
                         <div className='attribute'>
                            None
                         </div>
                     </div>
                     <div className='attribute-title'>
                        Sentiment analysis:
                         <div className='attribute'>
                            None
                         </div>
                     </div>
                     <div className='attribute-title'>
                        People detected:
                         <div className='attribute'>
                            None
                         </div>
                     </div>
                     <div className='attribute-title'>
                        Text detected:
                         <div className='attribute'>
                            None
                         </div>
                     </div>
                     <div className='attribute-title'>
                        Objects detected:
                         <div className='attribute'>
                            None
                         </div>
                     </div>
                     <div className='attribute-title'>
                        Map Square Information:
                         <div className='attribute'>
                            None
                         </div>
                     </div>
                 </div>
             </div>
             <Footer />
         </>);
     }
}
