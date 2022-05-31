import React from "react";
import PropTypes from "prop-types";
import {Navbar} from "../UILibrary/components";
import Footer from "../components/Footer";

// Images
import Clark_Catherine from "../../images/team/Clark_Catherine.jpg";
import Frampton_Stephanie from "../../images/team/Frampton_Stephanie.png";
import Ahmed_Ryaan from "../../images/team/Ahmed_Ryaan.jpg";
import Zimmer_Erica from "../../images/team/Zimmer_Erica.jpg";
import Fountain_Cole from "../../images/team/Fountain_Cole.jpg";
import Abraham_Igwe_Adanna from "../../images/team/Abraham-Igwe_Adanna.png";
import Akinbo_Tolulope from "../../images/team/Akinbo_Tolulope.jpg";
import Banerjee_Eesha from "../../images/team/Banerjee_Eesha.jpeg";
import Feliciano_Joshua from "../../images/team/Feliciano_Joshua.jpeg";
import Garcia_Raquel from "../../images/team/Garcia_Raquel.jpg";
import Garza_Montse from "../../images/team/Garza_Montse.jpg";
import He_Michelle from "../../images/team/He_Michelle.jpg";
import Huang_Peihua from "../../images/team/Huang_Peihua.jpg";
import Khaimov_Nicole from "../../images/team/Khaimov_Nicole.jpg";
import Lei_Ning_Er from "../../images/team/Lei_Ning-Er.jpg";
import Li_Felix from "../../images/team/Li_Felix.jpg";
import Lin_Jackie from "../../images/team/Lin_Jackie.jpeg";
import Lin_Jason from "../../images/team/Lin_Jason.jpg";
import Patel_Radha from "../../images/team/Patel_Radha.jpg";
import Patterson_Lydia from "../../images/team/Patterson_Lydia.jpeg";
import Romero_Sabrina from "../../images/team/Romero_Sabrina.jpg";
import Vidal_Justice from "../../images/team/Vidal_Justice.jpg";
import Wang_Rona from "../../images/team/Wang_Rona.png";
import Wang_Yifan from "../../images/team/Wang_Yifan.jpg";
import Weber_Dylan from "../../images/team/Weber_Dylan.jpg";
import Yang_Funing from "../../images/team/Yang_Funing.jpg";
import Zen_Hilary from "../../images/team/Zen_Hilary.jpg";
import Zheng_Vicky from "../../images/team/Zheng_Vicky.jpg";


const staffMembers = [
    {
        name: "Stephanie Frampton",
        title: "Faculty Director & Associate Professor of Literature",
        photoSrc: Frampton_Stephanie
    },
    {
        name: "Ryaan Ahmed",
        title: "Technical Director & Senior Research Engineer",
        photoSrc: Ahmed_Ryaan
    },
    {
        name: "Erica Zimmer",
        title: "Research Associate",
        photoSrc: Zimmer_Erica
    },
    {
        name: "Cole Fountain",
        title: "Administrative Assistant II",
        photoSrc: Fountain_Cole
    }
];

const studentMembers = [
    {
        name: "Adanna Abraham-Igwe",
        photoSrc: Abraham_Igwe_Adanna
    },
    {
        name: "Tolulope Akinbo",
        photoSrc: Akinbo_Tolulope
    },
    {
        name: "Eesha Banerjee",
        photoSrc: Banerjee_Eesha
    },
    {
        name: "Joshua Feliciano",
        photoSrc: Feliciano_Joshua
    },
    {
        name: "Raquel Garcia",
        photoSrc: Garcia_Raquel
    },
    {
        name: "Montse Garza",
        photoSrc: Garza_Montse
    },
    {
        name: "Michelle He",
        photoSrc: He_Michelle
    },
    {
        name: "Peihua Huang",
        photoSrc: Huang_Peihua
    },
    {
        name: "Nicole Khaimov",
        photoSrc: Khaimov_Nicole
    },
    {
        name: "Ning-Er Lei",
        photoSrc: Lei_Ning_Er
    },
    {
        name: "Felix Li",
        photoSrc: Li_Felix
    },
    {
        name: "Jackie Lin",
        photoSrc: Lin_Jackie
    },
    {
        name: "Jason Lin",
        photoSrc: Lin_Jason
    },
    {
        name: "Radha Patel",
        photoSrc: Patel_Radha
    },
    {
        name: "Lydia Patterson",
        photoSrc: Patterson_Lydia
    },
    {
        name: "Sabrina Romero",
        photoSrc: Romero_Sabrina
    },
    {
        name: "Justice Vidal",
        photoSrc: Vidal_Justice
    },
    {
        name: "Rona Wang",
        photoSrc: Wang_Rona
    },
    {
        name: "Yifan Wang",
        photoSrc: Wang_Yifan
    },
    {
        name: "Dylan Weber",
        photoSrc: Weber_Dylan
    },
    {
        name: "Funing Yang",
        photoSrc: Yang_Funing
    },
    {
        name: "Hilary Zen",
        photoSrc: Zen_Hilary
    },
    {
        name: "Vicky Zheng",
        photoSrc: Zheng_Vicky
    }
];

function TeamMember(props) {
    const className = props.isUROP
        ? "student-member col-12 col-sm-6 col-md-4 col-lg-3"
        : "staff-member col-12 col-md-6";

    const imgClassName = props.isUROP ? "student-img" : "staff-img";
    const nameClassName = props.isUROP ? "student-name" : "staff-name";
    return (
        <div className={className}>
            <img
                className={imgClassName}
                src={props.photoSrc}
                alt={props.name}
            />
            <div className={nameClassName}>
                {props.name}
            </div>
            {!props.isUROP &&
            <div className="job-title">
                {props.title}
            </div>
            }
        </div>
    );
}

TeamMember.propTypes = {
    isUROP: PropTypes.bool,
    name: PropTypes.string,
    title: PropTypes.string,
    photoSrc: PropTypes.string
};


class About extends React.Component {
    render() {
        return (<>
            <Navbar/>
            <div className="page">
                <div className="about-title">
                    About This Project
                </div>
                <div className="about-text">
                    <div className="prof-img-div text-wrap col-xs-2 col-sm-5 col-md-5 col-lg-3">
                        <figure className="figure text-center">
                            <img
                                className="prof-img"
                                src={Clark_Catherine}
                                alt="Catherine Clark"
                                align="left"
                            />
                            <div className="staff-name">Catherine Clark</div>
                            <figcaption className="figure-caption text-center">
                                Associate Professor of History and French Studies
                            </figcaption>
                        </figure>
                    </div>
                    <div>
                        <p>
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                            eiusmod tempor incididunt ut labore et dolore magna aliqua. Odio
                            eu feugiat pretium nibh ipsum consequat nisl vel pretium. Malesuada
                            nunc vel risus commodo viverra maecenas accumsan lacus vel. Cras
                            pulvinar mattis nunc sed blandit libero volutpat. Aliquam faucibus
                            purus in massa tempor nec feugiat nisl pretium. Quam nulla porttitor
                            massa id neque aliquam. Quam quisque id diam vel quam elementum
                            pulvinar etiam non. Etiam dignissim diam quis enim lobortis scelerisque
                            fermentum. Fringilla urna porttitor rhoncus dolor purus non. Vel
                            fringilla est ullamcorper eget nulla facilisi etiam. Tristique et
                            egestas quis ipsum suspendisse ultrices gravida. Vehicula ipsum a arcu
                            cursus vitae. Donec et odio pellentesque diam. Morbi tincidunt ornare
                            massa eget egestas purus viverra accumsan. Neque vitae tempus quam
                            pellentesque nec nam aliquam sem. Vitae congue mauris rhoncus aenean.
                        </p>
                        <p>
                            Suspendisse potenti nullam ac tortor. Ac auctor augue mauris augue
                            neque gravida in. Vitae sapien pellentesque habitant morbi tristique
                            senectus et netus. Pretium vulputate sapien nec sagittis. Ridiculus
                            mus mauris vitae ultricies leo integer. Magna sit amet purus gravida
                            quis blandit turpis cursus. Laoreet non curabitur gravida arcu ac
                            tortor dignissim convallis aenean. Eget aliquet nibh praesent tristique
                            magna sit. Tincidunt dui ut ornare lectus. Viverra justo nec ultrices
                            dui sapien eget mi proin. Nulla facilisi etiam dignissim diam. Vitae
                            justo eget magna fermentum.
                        </p>
                        <p>
                            Suspendisse potenti nullam ac tortor. Ac auctor augue mauris augue
                            neque gravida in. Vitae sapien pellentesque habitant morbi tristique
                            senectus et netus. Pretium vulputate sapien nec sagittis. Ridiculus
                            mus mauris vitae ultricies leo integer. Magna sit amet purus gravida
                            quis blandit turpis cursus. Laoreet non curabitur gravida arcu ac
                            tortor dignissim convallis aenean. Eget aliquet nibh praesent tristique
                            magna sit. Tincidunt dui ut ornare lectus. Viverra justo nec ultrices
                            dui sapien eget mi proin. Nulla facilisi etiam dignissim diam. Vitae
                            justo eget magna fermentum.
                        </p>
                    </div>
                </div>
                <div className="team">
                    <div className="about-title">Staff</div>
                    <div className="staff row">
                        {staffMembers.map((member, k) => (
                            <TeamMember
                                key={k}
                                isUROP={false}
                                name={member.name}
                                title={member.title}
                                photoSrc={member.photoSrc}
                            />
                        ))}
                    </div>
                    <div className="about-title">UROP Members</div>
                    <div className="students row">
                        {studentMembers.map((member, k) => (
                            <TeamMember
                                key={k}
                                isUROP={true}
                                name={member.name}
                                title={member.title}
                                photoSrc={member.photoSrc}
                            />
                        ))}
                    </div>
                </div>
            </div>
            <Footer/>
        </>);
    }
}

export default About;
