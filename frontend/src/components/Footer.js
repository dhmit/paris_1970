import React from "react";
import DHLogo from "../../images/logos/dh_logo.svg";
import MITLogo from "../../images/logos/mit_logo.svg";
import MellonLogo from "../../images/logos/mellon_logo.svg";

export class Footer extends React.Component {
    render() {
        return (
            <div className="row text-center footer">
                <div className="col-4 py-3">
                    <a href="https://digitalhumanities.mit.edu/">
                        <DHLogo/>
                    </a>
                </div>
                <div className="col-4 py-3">
                    <a href="https://www.mit.edu/">
                        <MITLogo/>
                    </a>
                </div>
                <div className="col-4 py-3">
                    <a href="https://www.mellon.org/">
                        <MellonLogo/>
                    </a>
                </div>
            </div>
        );
    }
}

export default Footer;
