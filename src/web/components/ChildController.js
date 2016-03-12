const React = require("react");
const Controller = require('./Controller.js');
const ToggleController = require('./ToggleController.js');


const ChildController = React.createClass({
    getInitialState: function() {
        return {is_manual: false};
    },
    componentDidMount: function() {
        this.props.session.call("box.controller.get_is_manual").then(function(res) {
            this.setState({is_manual: res});
        }.bind(this))
    },
    set_manual: function() {
        this.setState({is_manual: true});
        this.props.session.call("box.controller.set_is_manual", [true]);
    },
    set_auto: function() {
        this.setState({is_manual: false});
        this.props.session.call("box.controller.set_is_manual", [false]);
    },
    render: function() {
        var c = this.state.is_manual ? "alert-info" : "alert-warning";
        return <div className={"alert text-center " + c} role="alert">
            <p>Contrôlez vous même la température&nbsp;!</p>
            <br/>
            <ToggleController
                set_manual={this.set_manual}
                set_auto={this.set_auto}
                is_manual={this.state.is_manual}
                session={this.props.session}
                name={"Régulation"}
                topic={"box.regulation"}/>
            <br/>
            <Controller
                is_manual={this.state.is_manual}
                session={this.props.session}
                name={"Ventillation"}
                topic={"box.control.fan"}/>
            <br/>
            <Controller
                is_manual={this.state.is_manual}
                session={this.props.session}
                name={"Chauffage"}
                topic={"box.control.heater"}/>
        </div>
    }
});

module.exports = ChildController;
