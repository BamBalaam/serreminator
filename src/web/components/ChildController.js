const React = require("react");
const Controller = require('./Controller.js');
const ToggleController = require('./ToggleController.js');


const ChildController = React.createClass({
    getInitialState: function() {
        return {enabled: false};
    },
    enable: function() {
        this.setState({enabled: true});
    },
    disable: function() {
        this.setState({enabled: false});
    },
    render: function() {
        return <div className="alert alert-warning text-center" role="alert">
            <p>Contrôlez vous même la température&nbsp;!</p>
            <br/>
            <ToggleController
                enable={this.enable}
                disable={this.disable}
                disabled={!this.state.enabled}
                session={this.props.session}
                name={"Régulation"}
                topic={"box.regulation"}/>
            <br/>
            <Controller
                disabled={!this.state.enabled}
                session={this.props.session}
                name={"Ventillation"}
                topic={"box.fan"}/>
            <br/>
            <Controller
                disabled={!this.state.enabled}
                session={this.props.session}
                name={"Chauffage"}
                topic={"box.heater"}/>
        </div>
    }
});

module.exports = ChildController;
