import React from 'react';
import PropTypes from 'prop-types';
import { Navbar, Footer } from '../UILibrary/components';

const staffMembers = [
    {
        name: 'Stephanie Frampton',
        title: 'Faculty Director & Associate Professor of Literature',
        photoSrc: 'Frampton_Stephanie.png',
    },
    {
        name: 'Ryaan Ahmed',
        title: 'Technical Director & Senior Research Engineer',
        photoSrc: 'Ahmed_Ryaan.jpg',
    },
    {
        name: 'Erica Zimmer',
        title: 'Research Associate',
        photoSrc: 'Zimmer_Erica.jpg',
    },
    {
        name: 'Cole Fountain',
        title: 'Administrative Assistant II',
        photoSrc: 'Fountain_Cole.jpg',
    },
];

const studentMembers = [
    { name: 'Adanna Abraham-Igwe', photoSrc: 'Abraham-Igwe_Adanna.png' },
    { name: 'Tolulope Akinbo', photoSrc: 'Akinbo_Tolulope.jpg' },
    { name: 'Eesha Banerjee', photoSrc: 'Banerjee_Eesha.jpeg' },
    { name: 'Joshua Feliciano', photoSrc: 'Feliciano_Joshua.jpeg' },
    { name: 'Raquel Garcia', photoSrc: 'Garcia_Raquel.jpg' },
    { name: 'Montse Garza', photoSrc: 'Garza_Montse.jpg' },
    { name: 'Michelle He', photoSrc: 'He_Michelle.jpg' },
    { name: 'Peihua Huang', photoSrc: 'Huang_Peihua.jpg' },
    { name: 'Nicole Khaimov', photoSrc: 'Khaimov_Nicole.jpg' },
    { name: 'Ning-Er Lei', photoSrc: 'Lei_Ning-Er.jpg' },
    { name: 'Felix Li', photoSrc: 'Li_Felix.jpg' },
    { name: 'Jackie Lin', photoSrc: 'Lin_Jackie.jpeg' },
    { name: 'Jason Lin', photoSrc: 'Lin_Jason.jpg' },
    { name: 'Radha Patel', photoSrc: 'Patel_Radha.jpg' },
    { name: 'Lydia Patterson', photoSrc: 'Patterson_Lydia.jpeg' },
    { name: 'Sabrina Romero', photoSrc: 'Romero_Sabrina.jpg' },
    { name: 'Justice Vidal', photoSrc: 'Vidal_Justice.jpg' },
    { name: 'Rona Wang', photoSrc: 'Wang_Rona.png' },
    { name: 'Yifan Wang', photoSrc: 'Wang_Yifan.jpg' },
    { name: 'Dylan Weber', photoSrc: 'Weber_Dylan.jpg' },
    { name: 'Funing Yang', photoSrc: 'Yang_Funing.jpg' },
    { name: 'Hilary Zen', photoSrc: 'Zen_Hilary.jpg' },
    { name: 'Vicky Zheng', photoSrc: 'Zheng_Vicky.jpg' },
];

function TeamMember(props) {
    const className = props.isUROP
        ? 'student-member col-12 col-sm-6 col-md-4 col-lg-3'
        : 'staff-member col-12 col-md-6';

    const imgClassName = props.isUROP ? 'student-img' : 'staff-img';
    const nameClassName = props.isUROP ? 'student-name' : 'staff-name';
    return (
        <div className={className} >
            <img
                className={imgClassName}
                src={'/static/img/team/' + props.photoSrc}
                alt={props.name}
            />
            <div className={nameClassName}>
                {props.name}
            </div>
            {!props.isUROP
                && <div className='job-title'>
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
    photoSrc: PropTypes.string,
};


class About extends React.Component {
    render() {
        return (<>
            <Navbar />
            <div className='page'>
                <div className='about-title'>
                    About This Project
                </div>
                <div className='about-text'>
                    <div className='prof-img-div text-wrap col-xs-2 col-sm-5 col-md-5 col-lg-3'>
                        <figure className="figure text-center">
                            <img
                                className='prof-img'
                                src={'/static/img/team/Clark_Catherine.jpg'}
                                alt='Catherine Clark'
                                align='left'
                            />
                            <div className='staff-name'>Catherine Clark</div>
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
                <div className='team'>
                    <div className='about-title'>Staff</div>
                    <div className='staff row'>
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
                    <div className='about-title'>UROP Members</div>
                    <div className='students row'>
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
            <Footer />
        </>);
    }
}

export default About;
