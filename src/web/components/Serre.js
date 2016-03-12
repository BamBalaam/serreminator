const React = require("react");
const Graph = require('./Graph.js');
const Value = require('./Value.js');

const opts = {
    topic: "sensor.lux",
    id: "serre",
    PIDtarget: "pid.input.light",
    name: "Luminosité",
    unity: "Lux",
    PIDsetter: "pid.light.set_target",
    max: 900,
    min: 0
}

const Serre = React.createClass({
    render: function() {
        console.log("Render Serre");
        return <div>
            <div className="col-md-9">
                <Graph {...opts} session={this.props.session}/>
            </div>

            <div className="col-md-3">
                <Value {...opts} session={this.props.session}/>
            </div>
        </div>;
    }
});

module.exports = Serre;


