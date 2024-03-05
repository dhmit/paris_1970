import React from "react";
import {Modal, Button, Row, Col} from "react-bootstrap";
import { Trans, withTranslation } from "react-i18next";
import { Embed } from "../translation/translate";


//Images
import Car from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_008.jpg";
import Logo_Gif from "../images/gif/rec-animation-english---Copy.gif";
import Map_Page from "../images/featured/map page.png";
import Staring_Man from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_024.jpg";
import Walking_Man from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_078.jpg";
// import House from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_030.jpg";
// import Roof from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_002.jpg";
// import Neighbourhood from "../images/featured/BHVP_PH_CetaitParis_DP_0122_01_012.jpg";


const WorkInProgressModal = ({showModal, handleClose, translator}) => {
    // const { t } = useTranslation();
    const t = translator;
    // const test = gettext("hello");

    return (
        <Modal show={showModal} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>{t('HomePage.wipModal.title')}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {/* https://react.i18next.com/latest/trans-component */}
                <p><Trans
                    i18nKey='HomePage.wipModal.description1' // optional -> fallbacks to defaults if not provided
                    components={{
                        link1: <Embed href="https://digitalhumanities.mit.edu/" title="DH link"/>,
                        link2: <Embed href="https://history.mit.edu/people/catherine-clark/" title="Prof. Clark link"/>
                    }}
                /></p>
                <p>{t('HomePage.wipModal.description2')}</p>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    {t('HomePage.wipModal.close')}
                </Button>
            </Modal.Footer>
        </Modal>
    );
};


class BaseHomePage extends React.Component {
    state = {
        showModal: true
    };

    handleClose = () => this.setState({showModal: false});

    render() {

        return (<>
            <WorkInProgressModal showModal={this.state.showModal} handleClose={this.handleClose} translator={this.props.t}/>

            <section className="home-hero-section">
                <div className="main-section" style={{backgroundImage: `url(${Car})`}}>
                    <img src={Logo_Gif} alt="Paris Logo"/>
                    <div className="scroll-down">
                        {this.props.t('HomePage.scrollDown')}
                    </div>
                </div>
            </section>

            <section className="home-sections">
                <a href="/explore/">
                    <Row className="section-row photo-archive gx-0">
                        <Col sm={4} className="home-section-text">
                            <h2 className="h4">
                                {this.props.t('HomePage.explore')}
                            </h2>
                            <span className="large-arrow right">⟶</span>
                        </Col>
                        <Col sm={8} className="home-section-photo" style={{ backgroundImage: `url(${Walking_Man})` }} />
                    </Row>
                </a>

                <a href="/map/">
                    <Row className="section-row map-section gx-0">
                        <Col sm={8} className="home-section-photo"
                            style={{
                                backgroundImage: `url(${Map_Page})`,
                            }}
                        />
                        <Col sm={4} className="home-section-text">
                            <h2 className="h4">{this.props.t('HomePage.view')}</h2>
                            <span className="large-arrow left">⟵</span>
                        </Col>
                    </Row>
                </a>

                <a href="/articles/">
                    <Row className="section-row context gx-0">
                        <Col xs={8} sm={4} className="home-section-text">
                            <h2 className="h4">{this.props.t('HomePage.context')}</h2>
                            <span className="large-arrow right">⟶</span>
                        </Col>
                        <Col xs={4} sm={8} className="home-section-photo"
                            style={{
                                backgroundImage: `url(${Staring_Man})`,
                            }}
                        />
                    </Row>
                </a>

                <a href="/about/">
                    <Row className="section-row map-section gx-0">
                        <Col sm={8} className="home-section-photo"
                            style={{
                                backgroundImage: `url(${Map_Page})`,
                            }}
                        />
                        <Col sm={4} className="home-section-text">
                            <h2 className="h4">{this.props.t('HomePage.about')}</h2>
                            <span className="large-arrow left">⟵</span>
                        </Col>
                    </Row>
                </a>


            </section>

        </>);
    }
}

export const HomePage = withTranslation()(BaseHomePage);