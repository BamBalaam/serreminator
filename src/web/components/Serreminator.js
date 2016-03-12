const React = require("react");
const Serre = require('./Serre.js');

const Serreminator = React.createClass({
    getInitialState: function(){
        return {visible: "serre"};
    },
    onClickSerre: function(){
        this.setState({visible: "serre"});
    },
    onClickBox: function(){
        this.setState({visible: "box"});
    },
    render: function() {
        console.log("Render Serreminator");

        var content;
        if(this.state.visible == "serre"){
            content = <Serre
                session={this.props.session}
                topic="sensor.lux"
                id="serre"
                PIDtarget="pid.input.light"
                name="Luminosité"
                unity="Lux"
                PIDsetter="pid.light.set_target"
                max={900} min={0}/>
        }
        else {
            content = <Serre
                session={this.props.session}
                topic="sensor.box_temp"
                id="boite"
                PIDtarget="pid.input.temp"
                name="Température"
                unity="°C"
                PIDsetter="pid.temp.set_target"
                max={60} min={0}/>
        }
        return <div>
                <nav className="navbar navbar-default">
                    <div className="container-fluid">
                        <div className="navbar-header">
                            <a className="navbar-brand" href="#">
                                <img alt="Serreminator" src="logo.png" height="50"/>
                            </a>
                            <p className="navbar-text"><strong>Serreminator</strong> - Contrôle en temps réel</p>
                        </div>
                        <ul className="nav navbar-nav navbar-right">
                            <li className="navbar-btn">
                                <button
                                    className={"btn " + (this.state.visible == "serre" ? "btn-primary": "btn-default")}
                                    onClick={this.onClickSerre}>
                                    <i className="glyphicon glyphicon-leaf"></i>&nbsp;
                                    Serre
                                </button>
                            </li>
                            <li className="navbar-text">&nbsp;</li>
                            <li className="navbar-btn">
                                <button
                                    className={"btn " + (this.state.visible == "box" ? "btn-primary": "btn-default")}
                                    onClick={this.onClickBox}>
                                    <i className="glyphicon glyphicon-inbox"></i>&nbsp;
                                    Boite
                                </button>
                            </li>
                            <li className="navbar-text">&nbsp;</li>
                        </ul>
                    </div>
                </nav>
                <div className="container">
                    <div className="row">
                        <div className="tab-content">
                            {content}
                        </div>
                    </div>
                </div>
        </div>;
    }
});

module.exports = Serreminator;
