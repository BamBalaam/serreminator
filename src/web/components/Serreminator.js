const React = require("react");
const Serre = require('./Serre.js');
const Box = require('./Box.js');

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
        var content =
            <div className="tab-content">
                <div hidden={this.state.visible != 'serre'}>
                    <Serre session={this.props.session} />
                </div>
                <div hidden={this.state.visible != 'box'}>
                <Box session={this.props.session} />
                </div>
            </div>

        return <div>
                <nav className="navbar navbar-default">
                    <div className="container-fluid">
                        <div className="navbar-header">
                            <a className="navbar-brand" href="#">
                                <img alt="Serreminator" src="logo.png" height="50"/>
                            </a>
                            <p className="navbar-text">
                                <strong>Serreminator</strong> - Contrôle en temps réel d&#39;une serre
                            </p>
                        </div>
                        <ul className="nav navbar-nav navbar-right">
                            <li className="navbar-text" style={{opacity: 0.4}}>
                                Anthony <span style={{"font-variant": "small-caps"}}>Caccia</span>,
                                Andre Madeira <span style={{"font-variant": "small-caps"}}>Cortes</span>,
                                Romain <span style={{"font-variant": "small-caps"}}>Fontaine</span>,
                                Nikita <span style={{"font-variant": "small-caps"}}>Marchant</span>
                            </li>
                            <li className="navbar-text">&nbsp;&nbsp;</li>
                            <li className="navbar-btn">
                                <button
                                    className={"btn " + (this.state.visible == "serre" ? "btn-success": "btn-default")}
                                    onClick={this.onClickSerre}>
                                    <i className="glyphicon glyphicon-leaf"></i>&nbsp;
                                    Serre
                                </button>
                            </li>
                            <li className="navbar-text">&nbsp;</li>
                            <li className="navbar-btn">
                                <button
                                    className={"btn " + (this.state.visible == "box" ? "btn-success": "btn-default")}
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
                            {content}
                    </div>
                </div>
        </div>;
    }
});

module.exports = Serreminator;
