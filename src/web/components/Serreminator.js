const React = require("react");
const Serre = require('./Serre.js');

const Serreminator = React.createClass({
    render: function() {
        console.log("Render Serreminator");
        return <div>
                <nav className="navbar navbar-default">
                    <div className="container-fluid">
                    <div className="navbar-header">
                    <a className="navbar-brand" href="#">
                    <img alt="Serreminator" src="..."/>
                    </a>
                    <p className="navbar-text">Contrôle en temps réel</p>
                    </div>
                    </div>
                </nav>
                <div className="container">
                    <div className="row">
                        <div className="tab-content">
                            <Serre
                                session={this.props.session}
                                topic="sensor.lux"
                                id="serre"
                                PIDtarget="pid.input.light"
                                name="Luminosité"
                                unity="Lux"
                                PIDsetter="pid.light.set_target"
                                max={1200} min={0}/>
                            <Serre
                                session={this.props.session}
                                topic="sensor.temp"
                                id="boite"
                                PIDtarget="pid.input.temp"
                                name="Température"
                                unity="°C"
                                PIDsetter="pid.temp.set_target"
                                max={60} min={0}/>
                        </div>
                    </div>
                </div>
        </div>;
    }
});

module.exports = Serreminator;
