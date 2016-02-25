const React = require("react");
const Metric = require('./Metric.js');
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
                        <ul className="nav nav-tabs col-md-12" role="tablist">
                            <li className="active"><a href="#home" data-toggle="tab">Serre</a></li>
                            <li><a href="#profile" data-toggle="tab">Boite</a></li>
                        </ul>
                    </div>

                    <div className="row">
                        <div className="tab-content">
                            <Serre session={this.props.session} />
                        </div>
                    </div>
                </div>
        </div>;
    }
});

module.exports = Serreminator;
