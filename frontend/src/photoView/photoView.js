import React from 'react';
import * as PropTypes from 'prop-types';
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
             <div>
                 <div className='imageView' style={{ padding: '100px 50px', float: 'left' }}>
                     <h2>Photo Title: {title}</h2>
                     <img width={500} height={500} src={src} alt={alt}/>
                     <br/>
                     <button onClick={() => this.flipPhoto()}> Flip photo </button>
                 </div>
                 <div className='imageInfo'
                     style={{ padding: '100px 50px', float: 'left', marginTop: 50 }}>
                     <div className='attributeTitle' style={{ fontWeight: 'bold' }}>
                        Photographer:
                     <div className='attribute'style={{ fontWeight: 'normal' }}>
                            None
                     </div>
                     </div>
                     <div className='attributeTitle' style={{ fontWeight: 'bold' }}>
                        Categories
                         <div className='attribute'style={{ fontWeight: 'normal' }}>
                            None
                         </div>
                     </div>
                     <div className='attributeTitle' style={{ fontWeight: 'bold' }}>
                        Whitespace
                         <div className='attribute'style={{ fontWeight: 'normal' }}>
                            None
                         </div>
                     </div>
                     <div className='attributeTitle' style={{ fontWeight: 'bold' }}>
                        Sentiment analysis:
                         <div className='attribute'style={{ fontWeight: 'normal' }}>
                            None
                         </div>
                     </div>
                     <div className='attributeTitle' style={{ fontWeight: 'bold' }}>
                        People detected:
                         <div className='attribute'style={{ fontWeight: 'normal' }}>
                            None
                         </div>
                     </div>
                     <div className='attributeTitle' style={{ fontWeight: 'bold' }}>
                        Text detected:
                         <div className='attribute'style={{ fontWeight: 'normal' }}>
                            None
                         </div>
                     </div>
                     <div className='attributeTitle' style={{ fontWeight: 'bold' }}>
                        Objects detected:
                         <div className='attribute'style={{ fontWeight: 'normal' }}>
                            None
                         </div>
                     </div>
                     <div className='attributeTitle' style={{ fontWeight: 'bold' }}>
                        Map Square Information:
                         <div className='attribute'style={{ fontWeight: 'normal' }}>
                            None
                         </div>
                     </div>
                 </div>
             </div>
             <Footer />
         </>);
     }
}
PhotoView.propTypes = {
    id: PropTypes.number,
};
