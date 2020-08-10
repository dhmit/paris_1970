import React from 'react';
import PropTypes from 'prop-types';
import Navbar from './Navbar';
import { Footer } from '../UILibrary/components';

const staffMembers = [
    {
        name: 'Stephanie Frampton',
        title: 'Faculty Director & Associate Professor of Literature',
        photoSrc: 'stephanie_frampton.jpg',
    },
    {
        name: 'Ryaan Ahmed',
        title: 'Technical Director & Senior Research Engineer',
        photoSrc: 'ryaan_ahmed.jpg',
    },
    {
        name: 'Erica Zimmer',
        title: 'Research Associate',
        photoSrc: 'erica_zimmer.jpg',
    },
    {
        name: 'Nicole Fountain',
        title: 'Administrative Assistant II',
        photoSrc: 'nicole_fountain.jpg',
    },
];

const studentMembers = [
    {
        name: 'Jason Lin',
        photoSrc: 'jason_lin.jpg',
    },
    {
        name: 'Justice Vidal',
        photoSrc: 'justice_vidal.jpg',
    },
    {
        name: 'Michelle He',
        photoSrc: 'michelle_he.jpg',
    },
    {
        name: 'Ning-Er Lei',
        photoSrc: 'ning-er_lei.jpg',
    },
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
            <div className='page'>
                <Navbar currentPage='about'/>
                <div className='about-title'>
                    About This Project
                </div>
                <div className='about-text'>
                    <div className='evan-img-div text-wrap col-xs-2 col-sm-5 col-md-5 col-lg-3'>
                        <figure className="figure text-center">
                            <img
                                className='catherine-img'
                                src={'/static/img/team/catherine_clark.jpg'}
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
                            Copy about the project will go here.
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
