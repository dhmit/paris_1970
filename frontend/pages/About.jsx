import React from "react";
import { Container, Row, Col, Image, Figure, Card } from 'react-bootstrap';

import Footer from "../components/Footer";
import TitleDecoratorContainer from "../components/TitleDecoratorContainer";
import { Embed } from "../translation/translate";
import { Trans, withTranslation } from "react-i18next";
import about_page_right_citylist from "../images/about_page_right_citylist.svg?url";
import about_page_right_cropped_map from "../images/about_page_right_cropped_map.svg?url";
import about_page_right_image from "../images/about_page_right_image.svg?url";

/*import TitleDecorator from "../images/logos/title_decorator.svg"; */

// Images
import Clark_Catherine from "../images/team/Clark_Catherine.jpg";
import Frampton_Stephanie from "../images/team/Frampton_Stephanie.png";
import Ahmed_Ryaan from "../images/team/Ahmed_Ryaan.jpg";
import Zimmer_Erica from "../images/team/Zimmer_Erica.jpg";
import Fountain_Cole from "../images/team/Fountain_Cole.jpg";
import Abraham_Igwe_Adanna from "../images/team/Abraham-Igwe_Adanna.png";
import Akinbo_Tolulope from "../images/team/Akinbo_Tolulope.jpg";
import Banerjee_Eesha from "../images/team/Banerjee_Eesha.jpeg";
import Feliciano_Joshua from "../images/team/Feliciano_Joshua.jpeg";
import Garcia_Raquel from "../images/team/Garcia_Raquel.jpg";
import Garza_Montse from "../images/team/Garza_Montse.jpg";
import He_Michelle from "../images/team/He_Michelle.jpg";
import Huang_Peihua from "../images/team/Huang_Peihua.jpg";
import Khaimov_Nicole from "../images/team/Khaimov_Nicole.jpg";
import Lei_Ning_Er from "../images/team/Lei_Ning-Er.jpg";
import Li_Felix from "../images/team/Li_Felix.jpg";
import Lin_Jackie from "../images/team/Lin_Jackie.jpeg";
import Lin_Jason from "../images/team/Lin_Jason.jpg";
import Patel_Radha from "../images/team/Patel_Radha.jpg";
import Patterson_Lydia from "../images/team/Patterson_Lydia.jpeg";
import Romero_Sabrina from "../images/team/Romero_Sabrina.jpg";
import Vidal_Justice from "../images/team/Vidal_Justice.jpg";
import Wang_Rona from "../images/team/Wang_Rona.png";
import Wang_Yifan from "../images/team/Wang_Yifan.jpg";
import Weber_Dylan from "../images/team/Weber_Dylan.jpg";
import Yang_Funing from "../images/team/Yang_Funing.jpg";
import Zen_Hilary from "../images/team/Zen_Hilary.jpg";
import Zheng_Vicky from "../images/team/Zheng_Vicky.jpg";

const staffMembers = [
    {
        name: "Stephanie Frampton",
        title: "Faculty Director & Associate Professor of Literature",
        photoSrc: Frampton_Stephanie,
    },
    {
        name: "Stephanie Frampton",
        title: "Faculty Director & Associate Professor of Literature",
        photoSrc: Frampton_Stephanie,
    },
    {
        name: "Ryaan Ahmed",
        title: "Technical Director & Senior Research Engineer",
        photoSrc: Ahmed_Ryaan,
    },
    {
        name: "Erica Zimmer",
        title: "Research Associate",
        photoSrc: Zimmer_Erica,
    },
    {
        name: "Cole Fountain",
        title: "Administrative Assistant II",
        photoSrc: Fountain_Cole,
    },
];

const studentMembers = [
    {
        name: "Adanna Abraham-Igwe",
        photoSrc: Abraham_Igwe_Adanna,
    },
    {
        name: "Tolulope Akinbo",
        photoSrc: Akinbo_Tolulope,
    },
    {
        name: "Eesha Banerjee",
        photoSrc: Banerjee_Eesha,
    },
    {
        name: "Joshua Feliciano",
        photoSrc: Feliciano_Joshua,
    },
    {
        name: "Raquel Garcia",
        photoSrc: Garcia_Raquel,
    },
    {
        name: "Montse Garza",
        photoSrc: Garza_Montse,
    },
    {
        name: "Michelle He",
        photoSrc: He_Michelle,
    },
    {
        name: "Peihua Huang",
        photoSrc: Huang_Peihua,
    },
    {
        name: "Nicole Khaimov",
        photoSrc: Khaimov_Nicole,
    },
    {
        name: "Ning-Er Lei",
        photoSrc: Lei_Ning_Er,
    },
    {
        name: "Felix Li",
        photoSrc: Li_Felix,
    },
    {
        name: "Jackie Lin",
        photoSrc: Lin_Jackie,
    },
    {
        name: "Jason Lin",
        photoSrc: Lin_Jason,
    },
    {
        name: "Radha Patel",
        photoSrc: Patel_Radha,
    },
    {
        name: "Lydia Patterson",
        photoSrc: Patterson_Lydia,
    },
    {
        name: "Sabrina Romero",
        photoSrc: Romero_Sabrina,
    },
    {
        name: "Justice Vidal",
        photoSrc: Vidal_Justice,
    },
    {
        name: "Rona Wang",
        photoSrc: Wang_Rona,
    },
    {
        name: "Yifan Wang",
        photoSrc: Wang_Yifan,
    },
    {
        name: "Dylan Weber",
        photoSrc: Weber_Dylan,
    },
    {
        name: "Funing Yang",
        photoSrc: Yang_Funing,
    },
    {
        name: "Hilary Zen",
        photoSrc: Zen_Hilary,
    },
    {
        name: "Vicky Zheng",
        photoSrc: Zheng_Vicky,
    },
    {
        name: "Amanda Paredes Rioboo",
        photoSrc: Zheng_Vicky
    },
    {
        name: "Disha Kohli",
        photoSrc: Ahmed_Ryaan,
    },

    {
        name: "Maggie Yao",
        photoSrc: Zen_Hilary,
    },
    {
        name: "Bukunmi Shodipo",
        photoSrc: Zheng_Vicky
    },
    {
        name: "Mena Filfil",
        photoSrc: Zheng_Vicky
    },
    {
        name: "Kelly Fang",
        photoSrc: Zheng_Vicky
    },
    {
        name: "Kamau Njendu",
        photoSrc: Zheng_Vicky
    },
    {
        name: "Supriya Lall",
        photoSrc: Zheng_Vicky
    },
    {
        name: "David Chaudhari",
        photoSrc: Zheng_Vicky
    },
    {
        name: "Cindy Zheng",
        photoSrc: Zheng_Vicky
    },
    {
        name: "Lisa Li-Liang",
        photoSrc: Zheng_Vicky
    },
    {
        name: "Kingston Lew",
        photoSrc: Zheng_Vicky,
    },
    {
        name: "Nisha Nkya",
        photoSrc: Zheng_Vicky
    },
    {
        name: "Vivian Chinoda",
        photoSrc: Zheng_Vicky
    },
    {
        name: "Amanda Paredes Rioboo",
        photoSrc: Zheng_Vicky
    },
    {
        name: "Disha Kohli",
        photoSrc: Ahmed_Ryaan
    },
    {
        name: "Maggie Yao",
        photoSrc: Zen_Hilary
    }
];



function TeamMember(props) {
    return (
        <Card className="mb-3" style={{ width: '18rem' }}>
            <Card.Body>
                <Card.Title>{props.name}</Card.Title>
                <Card.Text>Here is a paragraph about this person!</Card.Text>
            </Card.Body>
        </Card>
    );
}

class BaseAbout extends React.Component {
    render() {
        return (
            <>
                <Container id="aboutPage">

                    <Row>
                        <TitleDecoratorContainer title="About" />
                        <Col>
                            <p>{this.props.t('About.context1')}</p>
                            <p><Trans
                                i18nKey='About.context2' // optional -> fallbacks to defaults if not provided
                                components={{
                                    link1: <Embed href="/map" title="Map link"/>,
                                    link2: <Embed href="/explore" title="Explore link"/>,
                                    link3: <Embed href="/articles" title="Articles link"/>
                                }}
                            /></p>
                        </Col>
                    </Row>
                    <Row>
                        <TitleDecoratorContainer title="The Team" />
                        <p><Trans
                            i18nKey='About.team1' // optional -> fallbacks to defaults if not provided
                            components={{
                                link1: <Embed href="https://history.mit.edu/people/catherine-clark/" title="Prof. Clark link"/>,
                                link2: <Embed href="https://digitalhumanities.mit.edu/people/alumni" title="Alumni link"/>,
                                link3: <Embed href="https://digitalhumanities.mit.edu/people" title="People link"/>
                            }}
                        /></p>
                        <p><Trans
                            i18nKey='About.team2' // optional -> fallbacks to defaults if not provided
                            components={{
                                link1: <Embed href="https://www.paris.fr/lieux/bibliotheque-historique-de-la-ville-de-paris-bhvp-16" title="Library link"/>
                            }}
                        /></p>
                    </Row>
                </Container>
                <Footer />
            </>
        );
    }
}

const About = withTranslation()(BaseAbout)
export default About;
