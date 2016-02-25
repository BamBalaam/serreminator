const React = require("react");
const Graph = require('./Graph.js');
const Value = require('./Value.js');

const Serre = React.createClass({
    render: function() {
        console.log("Render Serre");
        return <div className="tab-pane active" id="home">
            <div className="col-md-9">
            <Graph session={this.props.session} topic="sensor.lux" PIDtarget="pid.input.light" name="Luminosité" unity="Lux" max={1200} min={0}/>
            </div>

            <div className="col-md-3">
            <Value session={this.props.session} topic="sensor.lux" PIDtarget="pid.input.light" unity="lux" PIDsetter="pid.set.ligth"/>
            </div>
            </div>;
    }
});

module.exports = Serre;
