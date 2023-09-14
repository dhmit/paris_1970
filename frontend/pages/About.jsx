import React from "react";
import { Container, Row, Col, Image, Figure, Card } from 'react-bootstrap';

import Footer from "../components/Footer";
import TitleDecoratorContainer from "../components/TitleDecoratorContainer";
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

class About extends React.Component {
    render() {
        return (
            <>
                <Container id="aboutPage">

                    <Row>
                        <TitleDecoratorContainer title="About" />
                        <Col>
                            <p>
                                In May 1970, thousands of amateur photographers spread out across Paris to take pictures. They were participants in a photo contest, “This was Paris in 1970,” organized by the cooperative electronics store the Fnac. Each contestant had been assigned to document a 250m square of the city. By the end of the month, this army of photographers had produced an unprecedented collection of 100,000 photographs: 70,000 black-and-white prints and 30,000 colors slides. This website currently hosts 5,000 color slides from the 13th and 19th arrondissements, areas of the city which were undergoing significant change in 1960s and 1970s.
                            </p>
                            <p>
                                The project This was Paris in 1970 provides tools to explore the rich archive: a <a href="/map">map</a> to see the photos square by square; an <a href="/explore">object detector</a> to search for photos of many objects from people to cats, cars to strollers; a similar photo viewer to identify photos by composition rather than subject; and <a href="/articles">articles</a> providing context and analysis.
                            </p>
                        </Col>
                    </Row>
                    <Row>
                        <TitleDecoratorContainer title="The Team" />
                        <p>
                        This is Paris in 1970 was created in MIT’s Digital Humanities Lab as a collaboration between DH Fellow <a href="https://history.mit.edu/people/catherine-clark/">Prof. Catherine Clark</a>, <a href="https://digitalhumanities.mit.edu/people/alumni">four dozen undergraduate research associates</a>, and <a href="https://digitalhumanities.mit.edu/people">the instructional staff</a> of the DH Lab. Justice Vidal built out the first version of the site, and Nina Li spearheaded the design work.
                        </p>
                        <p>
                            The <a href="https://www.paris.fr/lieux/bibliotheque-historique-de-la-ville-de-paris-bhvp-16">Bibliothèque historique de la Ville de Paris</a> holds the contest photographs. Its photo department made this project possible.
                        </p>
                    </Row>
                </Container>
                <Footer />
            </>
        );
    }
}

export default About;
